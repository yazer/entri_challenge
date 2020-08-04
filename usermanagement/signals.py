import random
import string

from django.db.models.signals import post_save
from django.dispatch import receiver

from usermanagement.models import (InterviewerProfile, CandidateProfile)


def random_string_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

@receiver(post_save, sender=InterviewerProfile)
@receiver(post_save, sender=CandidateProfile)
def create_unique_string(sender, instance, created, **kwargs):
    print("signal callledd for customer", sender)
    if created:
        print ("create")
        while(True):
            unique_string = random_string_generator()
            if not InterviewerProfile.objects.filter(user_uid=unique_string).exists():
                instance.user_uid = unique_string
                instance.save()
                break
    else:
        print ("update")
