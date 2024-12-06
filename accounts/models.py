from django.db import models
from django.contrib.auth.models import AbstractUser

class HuellaUser(AbstractUser):
    is_protector = models.BooleanField(default=False, help_text="Marcar si es una protectora")

    class Meta:
        db_table = 'huella_user'  # Prefijo para diferenciar
