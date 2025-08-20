from rest_framework import serializers
from .models import audioJob, Transcript, usageLog


class audioJobSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    transcript = serializers.SerializerMethodField()

    class Meta:
        model = audioJob
        fields = ['__all__']

        read_only_fields = ['id', 'user', 'status', 'progress', 'error_message', 'cost', 'minutes_processed', 'created_at', 'updated_at', 'completed_at', 'transcript']

        def get_transcript(self, obj):
            if hasattr(obj, 'transript'):
                return transcriptSerializer(obj.transcript).data
            return None
        
class transcriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['__all__']
        read_only_fields = ['id', 'audio_job', 'created_at', 'updated_at']

class usageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = usageLog
        fields = ['__all__']
        read_only_fields = ['id', 'user', 'audio_job', 'created_at']