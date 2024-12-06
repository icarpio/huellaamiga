from django.urls import path
from .views import edit_protector, add_animal, send_message, inbox

urlpatterns = [
    path('edit_protector/', edit_protector, name='edit_protector'),
    path('add-animal/', add_animal, name='add_animal'),
    path('send-message/<int:protector_id>/', send_message, name='send_message'),
    path('inbox/', inbox, name='inbox'),
]
