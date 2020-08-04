from django.contrib import admin

from usermanagement.models import (InterviewerProfile, CandidateProfile,
                                    InterviewSlot)

admin.site.register(InterviewerProfile)
admin.site.register(CandidateProfile)
admin.site.register(InterviewSlot)