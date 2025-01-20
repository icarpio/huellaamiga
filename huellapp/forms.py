from django import forms
from .models import Animal, Messageha,Protector
from django.contrib.auth import get_user_model

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'age', 'description', 'image']  # Excluye 'protector'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class MessageForm(forms.ModelForm):
    class Meta:
        model = Messageha
        fields = ['content']
        
class ProtectorForm(forms.ModelForm):
    class Meta:
        model = Protector
        fields = ['name', 'location', 'logo']
        
class CustomUserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name'] 