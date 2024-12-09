from django.urls import path
from .views import *

urlpatterns = [
    path('add_animal/', add_animal, name='add_animal'),
    path('inbox/', inbox, name='inbox'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('edit_protector/', edit_protector, name='edit_protector'),
    path('create_protector/', create_protector, name='create_protector'),
    path('conversation/<int:conversation_id>/', view_conversation, name='view_conversation'),
    path('send_message/<int:recipient_id>/', send_message, name='send_message'),
    path('animals/', protector_animals, name='protector_animals'),
    path('animals/edit/<int:animal_id>/', edit_animal, name='edit_animal'),
]


