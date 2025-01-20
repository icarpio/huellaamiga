from django.shortcuts import render, redirect
from .models import Protector,Conversation, Animal
from .forms import AnimalForm, MessageForm,ProtectorForm,CustomUserEditForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied


@login_required
def add_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save(commit=False)
            # Asignar el protector automáticamente al usuario actual
            animal.protector = Protector.objects.get(user=request.user)  # Obtener el protector del usuario
            animal.save()
            return redirect('index')  # Redirigir a la lista de animales (ajusta la URL)
    else:
        form = AnimalForm()

    return render(request, 'huellapp/add_animal_min.html', {'form': form})

@login_required
def create_protector(request):
    if request.method == 'POST':
        form = ProtectorForm(request.POST, request.FILES)
        if form.is_valid():
            protector = form.save(commit=False)
            protector.user = request.user  # Asignar el usuario actual
            protector.save()
            return redirect('index')  # Redirigir al home
    else:
        form = ProtectorForm()
    
    return render(request, 'huellapp/edit_protector.html', {'form': form})

@login_required
def edit_protector(request):
    # Intentar obtener la protectora asociada al usuario
    try:
        protector = Protector.objects.get(user=request.user)
    except Protector.DoesNotExist:
        # Si no existe un protector, redirigir a la vista de crear protector
        return redirect('create_protector')

    if request.method == 'POST':
        form = ProtectorForm(request.POST, request.FILES, instance=protector)
        if form.is_valid():
            form.save()
            return redirect('protector_animals')  # Redirigir a la página de perfil
    else:
        form = ProtectorForm(instance=protector)
    return render(request, 'huellapp/edit_protector.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('index')  # Redirigir a la página de perfil u otra vista
    else:
        form = CustomUserEditForm(instance=request.user)  # Prellenar el formulario con los datos actuales

    return render(request, 'huellapp/edit_profile.html', {'form': form})


User = get_user_model()
@login_required
def send_message(request, recipient_id):
    """
    Vista para enviar un mensaje entre usuarios (incluyendo protectoras).
    """
    # Obtener al destinatario, que es el usuario asociado a la protectora
    recipient_user = get_object_or_404(User, id=recipient_id)
    
    # Verificar si el destinatario es una protectora
    protector = Protector.objects.filter(user=recipient_user).first()

    # Crear o buscar una conversación existente entre el usuario que envía el mensaje y el destinatario
    conversation = Conversation.objects.filter(
        sender=request.user, recipient=recipient_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.filter(
            sender=recipient_user, recipient=request.user
        ).first()

    if not conversation:
        conversation = Conversation.objects.create(sender=request.user, recipient=recipient_user)

    # Manejar el formulario de mensaje
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            # Crear el mensaje pero no guardarlo aún
            message = form.save(commit=False)
            message.sender = request.user  # Usuario que envía el mensaje
            message.conversation = conversation  # Asignar la conversación
            message.save()  # Guardar el mensaje en la base de datos
            return redirect('view_conversation', conversation_id=conversation.id)  # Redirigir a la conversación
        else:
            print("Errores en el formulario:", form.errors)
    else:
        form = MessageForm()  # Formulario vacío para GET

    # Renderizar la plantilla con los datos correctos
    return render(request, 'huellapp/send_message.html', {
        'form': form,
        'recipient': recipient_user,  # Aquí pasamos el usuario correcto
        'protector': protector,  # Datos de la protectora (si aplica)
    })


def inbox(request):
    # Obtener las conversaciones donde el usuario es remitente o destinatario
    conversations = Conversation.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-created_at')
    return render(request, 'huellapp/inbox.html', {'conversations': conversations})


User = get_user_model()

@login_required
def start_conversation(request, recipient_id):
    # Obtener la protectora (recipient)
    recipient = get_object_or_404(User, id=recipient_id)

    # Verificar si ya existe una conversación entre el usuario y la protectora
    conversation, created = Conversation.objects.get_or_create(
        sender=request.user,
        recipient=recipient
    )

    return redirect('view_conversation', conversation_id=conversation.id)



@login_required
def view_conversation(request, conversation_id):
    # Obtener la conversación donde el usuario es el sender o recipient
    conversation = get_object_or_404(
        Conversation, 
        id=conversation_id
    )

    # Verificar si el usuario actual es el sender o el recipient
    if conversation.sender != request.user and conversation.recipient != request.user:
        raise PermissionDenied  # Si no es ni el sender ni el recipient, denegar acceso

    # Obtener los mensajes de la conversación ordenados por timestamp
    messages = conversation.messages.all().order_by('timestamp')

    # Procesar el formulario de mensaje si es POST
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user  # El usuario actual envía el mensaje
            message.conversation = conversation  # Asociar el mensaje a la conversación
            message.save()
            return redirect('view_conversation', conversation_id=conversation.id)
    else:
        form = MessageForm()

    # Renderizar la conversación con los mensajes y el formulario
    return render(request, 'huellapp/view_conversation.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })



@login_required
def protector_animals(request):
    # Obtener la protectora asociada al usuario actual
    protector = get_object_or_404(Protector, user=request.user)
    # Filtrar los animales asociados a esta protectora
    animals = Animal.objects.filter(protector=protector)

    if request.method == 'POST':
        # Manejar eliminación de animales
        animal_id = request.POST.get('animal_id')
        if animal_id:
            animal = get_object_or_404(Animal, id=animal_id, protector=protector)
            animal.delete()
            return redirect('protector_animals')

    context = {
        'protector': protector,
        'animals': animals,
    }
    return render(request, 'huellapp/animals_list.html', context)

@login_required
def edit_animal(request, animal_id):
    # Obtener el animal que se quiere editar, asegurándose de que pertenece a la protectora del usuario
    animal = get_object_or_404(Animal, id=animal_id, protector__user=request.user)

    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect('protector_animals')  # Redirigir al listado de animales
    else:
        form = AnimalForm(instance=animal)

    context = {
        'form': form,
        'animal': animal,
    }
    return render(request, 'huellapp/edit_animal.html', context)