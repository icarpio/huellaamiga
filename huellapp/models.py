from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

class Protector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    logo = CloudinaryField('image', transformation=[
        {'width': 800, 'height': 600, 'crop': 'fill'}
    ], folder='huellamiga/protectors/', null=True, blank=True)  # Ahora el logo puede ser nulo y opcional en los formularios

    def __str__(self):
        return self.name

class Animal(models.Model):
    SPECIES_CHOICES = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('roedor', 'Roedor'),
        ('reptil', 'Reptil'),
    ]
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    age = models.IntegerField()
    description = models.TextField()
    protector = models.ForeignKey(Protector, on_delete=models.CASCADE)  # Relación con Protector, no con el usuario
    image = CloudinaryField('image', transformation=[
        {'width': 800, 'height': 600, 'crop': 'fill'}
    ], folder='huellamiga/animals/')  

    def __str__(self):
        return self.name

class Conversation(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sent_conversations'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='received_conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient')

    def __str__(self):
        return f"Conversation between {self.sender.username} and {self.recipient.username}"

class Messageha(models.Model):
    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name='messages',
        null=True,  # Hacer que el campo sea nulo temporalmente
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"

