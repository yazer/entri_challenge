from django.db import models
from django.contrib.auth.models import User

# Create your models here.

COUNTRY_CODE = (
    ('91', 'India'),
    )

class InterviewerProfile(models.Model):
    user = models.OneToOneField(User, related_name='staff_profile',on_delete = models.CASCADE)
    country_code = models.CharField(choices=COUNTRY_CODE, max_length=12, blank=True, default='91')
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, related_name='candidate_profile',on_delete = models.CASCADE)
    country_code = models.CharField(choices=COUNTRY_CODE, max_length=12, blank=True, default='91')
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class InterviewSlot(models.Model):
    interviewer = models.ForeignKey(InterviewerProfile, related_name='interviewer_slots', on_delete = models.CASCADE, null=True, blank=True)
    candidate = models.ForeignKey(CandidateProfile, related_name='candidate_slots', on_delete = models.CASCADE, null=True, blank=True)
    slot = models.DateTimeField()
    # timezone = models.CharField(max_length=32, null=True, blank=True)
    is_active = models.BooleanField(default=True)
