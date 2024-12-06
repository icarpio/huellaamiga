from django import forms
from .models import Animal, Messageha,Protector

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['name', 'species', 'age', 'description','image']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Messageha
        fields = ['content']
        

class ProtectorForm(forms.ModelForm):
    class Meta:
        model = Protector
        fields = ['name', 'location', 'logo']