from rest_framework import serializers
from django.contrib.auth.models import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'minutes_processed', 'total_cost', 'monthly_quota_minutes', 'quota_reset_date']
        read_only_fields = ['id', 'minutes_processed', 'total_cost', 'monthly_quota_minutes', 'quota_reset_date']


class userRegisterationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only = True, required = True, validators = [validate_password])
    password2 = serializers.CharField(write_only = True, required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'company', 'phone']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    
class userProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'company', 'phone']

        