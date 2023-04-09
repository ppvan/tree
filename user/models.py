import uuid
from pathlib import Path

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.

MEDIA_PATH = Path('avatars')


class Profile(models.Model):

    def get_path(instance, filename):
        extension = filename.split('.')[-1]
        uuid_name = uuid.uuid1().hex
        return MEDIA_PATH / f'{uuid_name}.{extension}'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    avatar = ProcessedImageField(upload_to=get_path,
                                 default='avatars/default.png',
                                 processors=[ResizeToFill(64, 64)],
                                 format='PNG',
                                 options={'quality': 60})
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


"""Django signals ~ Trigger a function when a model is saved
https://docs.djangoproject.com/en/4.1/topics/signals/
"""


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()