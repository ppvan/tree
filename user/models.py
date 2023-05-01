from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from imagekit.models import ProcessedImageField
from tree.utils import hashed_filename
from imagekit.processors import ResizeToFill

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    avatar = ProcessedImageField(
        upload_to=hashed_filename,
        default="avatars/default.png",
        processors=[ResizeToFill(64, 64)],
        format="PNG",
        options={"quality": 60},
    )
    bio = models.TextField(max_length=500, blank=True)

    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.username} Profile"


"""Django signals ~ Trigger a function when a model is saved
https://docs.djangoproject.com/en/4.1/topics/signals/
"""


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
