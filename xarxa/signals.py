# xarxa/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile  # Importa el teu model Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un Profile automàticament quan es crea un User."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  if instance.profile is not None:
    """Guarda el Profile quan es guarda el User."""
    instance.profile.save()
  else:
    """Si no hi ha un Profile, crea'n un nou."""
    Profile.objects.create(user=instance)
