from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone 

class User(AbstractUser):
    
    minutes_processed = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = 0.0,
        help_text = "Total minutes of audio processed"
    )

    total_cost = models.DecimalField(
        max_digits = 10,
        decimal_places = 4,
        default = 0.0,
        help_text = "Total cost in INR"
    )

    monthly_quota_minutes = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = 100.0,
        help_text = "Monthly quota in minutes"
    )

    quota_reset_date = models.DateField(
        default = timezone.now,
        help_text = "Date when monthly quota resets"
    )

    company = models.CharField(max_length = 100, blank = True)
    phone = models.CharField(max_length = 20, blank = True)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def get_remaining_Quota(self):
        if self.quota_reset_date.month != timezone.now().month:
            self.minutes_processed = 0
            self.quota_reset_date = timezone.now().date()
            self.save()
        return max(0, self.monthly_quota_minutes - self.minutes_processed)

    def can_process_audio(self, minutes):
        return self.get_remaining_Quota() >= minutes
