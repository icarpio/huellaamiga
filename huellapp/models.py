from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

class Protector(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    logo = CloudinaryField('image', transformation=[
        {'width': 800, 'height': 600, 'crop': 'fill'}
    ], folder='huellamiga/protectors/')

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
    protector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = CloudinaryField('image', transformation=[
        {'width': 800, 'height': 600, 'crop': 'fill'}
    ], folder='huellamiga/animals/')  

    def __str__(self):
        return self.name


class Messageha(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.timestamp}'
