from django.shortcuts import render
from django.shortcuts import render, redirect
from huellapp.models import Animal
from huellapp.forms import AnimalForm

def index(request):
    animals = Animal.objects.all()  # Obtener todos los animales
    if request.method == 'POST' and request.user.is_protector:
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.protector = request.user  # Asignar el protector actual
            animal.save()
            return redirect('home')  # Redirigir a la página de inicio
    else:
        form = AnimalForm() if request.user.is_protector else None

    return render(request, 'home/index.html', {'animals': animals, 'form': form})
