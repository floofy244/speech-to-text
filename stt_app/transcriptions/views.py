import os
import uuid
from decimal import Decimal
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from pydub import AudioSegment
from faster_whisper import WhisperModel
from .models import audioJob, Transcript, usageLog
from serializers import audioJobSerializer, transcriptSerializer, usageLogSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_audio(request):
    if 'audio_file' not in request.FILES:
        return Response({
            'error' : 'No audio file provided',
        }, status = status.HTTP_400_BAD_REQUEST)
    
    audio_file = request.FILES['audio_file']
    language = request.data.get('language', 'auto')
    model_size = request.data.get('model_size', 'base')

    allowed_types = ['audio/mpeg', 'audio/wav', 'audio/m4a', 'audio/ogg', 'audio/webm']

    if audio_file.content_type not in allowed_types:
        return Response({
            'error' : 'Invalid file type. Please upload an audio file.'
        }, status = status.HTTP_400_BAD_REQUEST)
    
    if audio_file.size > 100 * 1024 * 1024:
        return Response({
            'error' : 'File size is too large. Maximum size is 100MB.',
        }, status = status.HTTP_400_BAD_REQUEST)
    
    try:
        audio_job = audioJob.objects.create(
            user = request.user,
            original_filename = audio_file.name,
            language = language,
            model_size = model_size,
            file_size = audio_file.size,
            status = 'pending'
        )


        audio_job.audio_file.save(
            f"{uuid.uuid4()}_{audio_file.name}",
            audio_file
        )

        try:
            audio = AudioSegment.from_file(audio_job.audio_file.path)
            duration = len(audio) / 1000
            audio_job.duration = Decimal(str(duration))
            audio_job.save()

        except Exception as e:
            print(f"Error calculating duration: {e}")

        if audio_job.duration:
            minutes_needed = audio_job.duration / 60
            if not request.user.can_process_audio(minutes_needed):
                audio_job.status = 'failed'
                audio_job.error_message = 'Insufficient quota'
                audio_job.save()
                return Response({
                    'error' : 'Insufficient quota for this audio file'
                }, status = status.HTTP_400_BAD_REQUEST)
            
        transcribe_audio(audio_job)

        return Response({
            'message' : 'Audio Uploaded Successfully',
            'job_id' : audio_job.id,
            'status' : audio_job.status
        }, status = status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({
            'error' : str(e)
        }, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
def transcribe_audio(audio_job):
    
    try:
        audio_job.status = 'processing'
        audio_job.progress = 10
        audio_job.save()

        model = WhisperModel(audio_job.model_size, device = 'cpu', compute_type = 'int8')

        audio_job.progress = 30
        audio_job.save()

        segments, info = model.transcribe(
            audio_job.audio_file.path,
            language = audio_job.language if audio_job.language != 'auto' else None,
            word_timestamps = True
        )

        audio_job.progress = 70
        audio_job.save()


        text = ""
        word_segments = []

        for segment in segments:
            text += segment.text + " "
            for word in segment.words:
                word_segments.append({
                    'word' : word.word,
                    'start' : word.start,
                    'end' : word.end,
                    'probability' : word.probability
                })

        minutes_processed = audio_job.duration / 60 if audio_job.duration else 0

        cost_per_minute = {
            'tiny' : 0.09,
            'base' : 0.17,
            'small' : 0.35,
            'medium' : 0.70,
            'large' : 1.40,
        }

        cost = minutes_processed * cost_per_minute.get(audio_job.model_size, 0.002)

        transcript = Transcript.objects.create(
            audio_job = audio_job,
            text = text.strip(),
            segments = word_segments,
            language_detected = info.language,
            confidence_score = info.language_probability
        )

        audio_job.status = 'completed'
        audio_job.progress = 100
        audio_job.cost = cost
        audio_job.minutes_processed = minutes_processed
        audio_job.save()


        user = audio_job.user
        user.minutes_processed += minutes_processed
        user.total_cost = cost
        user.save()


        usageLog.objects.create(
            user = user,
            audio_job = audio_job,
            minutes_processed = minutes_processed,
            cost = cost,
            model_used = audio_job.model_size
        )

        generate_export_files(transcript)

    except Exception as e:
        audio_job.status = 'failed'
        audio_job.error_message = str(e)
        audio_job.save()

def generate_export_files(transcript):

    """Generate export files for the transcripts"""



