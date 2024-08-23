from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom User Model
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    public_visibility = models.BooleanField(default=False)

    @property
    def age(self):
        from datetime import date
        if self.birth_year:
            today = date.today()
            return today.year - self.birth_year
        return None

# Profile Model for additional user information
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=15, unique=True)

# Signal to create or update Profile when CustomUser is created or saved
@receiver(post_save, sender=CustomUser)
def create_or_update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        try:
            profile = instance.profile
            profile.save()
        except Profile.DoesNotExist:
            Profile.objects.create(user=instance)
