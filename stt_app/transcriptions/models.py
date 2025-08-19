from django.db import models
import os
import uuid 
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()

def audio_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('audio', filename)

def transcript_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('transcipts', filename)


class audioJob(models.Model):
    STATUS_CHOICES = {
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    }

    LANGUAGE_CHOICES = {
        ('en', 'English'),
        ('es', 'Spanish'),
        ('de', 'German'),
        ('it', 'Italian'),
        ('pt', 'Portuguese'),
        ('ru', 'Russian'),
        ('ja', 'Japanese'),
        ('ko', 'Korean'),
        ('zh', 'Chinese'),
        ('auto', 'Auto-detect'),
    }

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'audio_jobs')

    original_filename = models.CharField(max_length = 255)
    audio_file = models.FileField(upload_to = audio_file_path, null = True, blank = True)
    s3_key = models.CharField(max_length = 500, null = True, blank = True)
    file_size = models.BigIntegerField(null = True, blank = True)
    duration = models.DecimalField(max_digits = 20, decimal_places = 2, null = True, blank = True)

    language = models.CharField(max_length = 10, choices = LANGUAGE_CHOICES, default = 'auto')
    model_size = models.CharField(max_length = 20, default = 'base', choices = [('tiny', 'Tiny'), ('base', 'Base'), ('small', 'Small'), ('medium', 'Medium'), ('large', 'Large')])

    status = models.CharField(max_length = 20, choices = STATUS_CHOICES, default = 'pending')
    progress = models.IntegerField(default=0) # 0  to 100
    error_message = models.TextField(blank = True)

    cost = models.DecimalField(max_digits = 10, decimal_places = 4, default = 0.0)
    minutes_processed = models.DecimalField(max_digits = 10, decimal_places = 2, default = 0.0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    completed_at = models.DateTimeField(null = True, blank = True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.original_filename} - {self.status}"
    
    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()

        super().save(*args, **kwargs)


class Transcript(models.Model):

    FORMAT_CHOICES = [
        ('txt', 'Plain Text'),
        ('srt', 'SRT Subtitles'),
        ('vtt', 'WebVTT'),
        ('json', 'JSON'),
    ]

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    audio_job = models.OneToOneField(audioJob, on_delete = models.CASCADE, related_name = 'Transcript')

    text = models.TextField()
    segments = models.JSONField(default = list)
    language_detected = models.CharField(max_length = 10, null = True, blank = True)
    confidence_score = models.DecimalField(max_digits = 5, decimal_places = 4, null = True, blank = True)


    txt_file = models.FileField(upload_to = transcript_file_path, null = True, blank = True)
    srt_file = models.FileField(upload_to = transcript_file_path, null = True, blank = True)
    vtt_file = models.FileField(upload_to = transcript_file_path, null = True, blank = True)
    json_file = models.FileField(upload_to = transcript_file_path, null = True, blank = True)

    txt_s3_key = models.CharField(max_length = 500, null = True, blank = True)
    vtt_s3_key = models.CharField(max_length = 500, null = True, blank = True)
    srt_s3_key = models.CharField(max_length = 500, null = True, blank = True)
    json_s3_key = models.CharField(max_length = 500, null = True, blank = True)


    word_count = models.IntegerField(default = 0)
    character_count = models.IntegerField(default = 0)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Transcript for {self.audio_job.original_filename}"
    
    def save(self, *args, **kwargs):
        if self.text:
            self.word_count = len(self.text.split())
            self.character_count = len(self.text)

        super().save(*args, **kwargs)


class usageLog(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'usage_logs')
    audio_job = models.ForeignKey(audioJob, on_delete = models.CASCADE, related_name = 'usage_logs')

    minutes_processed = models.DecimalField(max_digits = 10, decimal_places = 2)
    cost = models.DecimalField(max_digits = 10, decimal_places = 4)
    model_used = models.CharField(max_length = 20)

    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.minutes_processed}min - ₹{self.cost}"
    
    