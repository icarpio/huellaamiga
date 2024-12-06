from django.shortcuts import render, redirect
from .models import Protector, Animal, Messageha
from .forms import AnimalForm, MessageForm,ProtectorForm
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save(commit=False)
            animal.protector = request.user.protector  # Asumiendo que el usuario tiene un perfil de protector
            animal.save()
            return redirect('animal_list')
    else:
        form = AnimalForm()
    return render(request, 'huellapp/add_animal.html', {'form': form})


def send_message(request, recipient_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        recipient = settings.AUTH_USER_MODEL.objects.get(id=recipient_id)
        Messageha.objects.create(sender=request.user, recipient=recipient, content=content)
        return redirect('inbox')  # Redirige a la bandeja de entrada
    return render(request, 'huellapp/send_message.html', {'recipient_id': recipient_id})

def inbox(request):
    messages = Messageha.objects.filter(recipient=request.user).order_by('-timestamp')
    return render(request, 'huellapp/inbox.html', {'messages': messages})

@login_required
def edit_protector(request):
    # Obtener la protectora asociada al usuario
    protector = get_object_or_404(Protector, user=request.user)

    if request.method == 'POST':
        form = ProtectorForm(request.POST, request.FILES, instance=protector)
        if form.is_valid():
            form.save()
            return redirect('protector_profile')  # Redirigir a la página de perfil, por ejemplo.
    else:
        form = ProtectorForm(instance=protector)
    
    return render(request, 'huellapp/edit_protector.html', {'form': form})