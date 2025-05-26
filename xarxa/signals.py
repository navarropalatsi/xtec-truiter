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
  try:
    instance.profile.save()  # Intenta guardar el perfil
  except Profile.DoesNotExist:
    # Si no existeix, crea'l (cas excepcional)
    Profile.objects.create(user=instance)
