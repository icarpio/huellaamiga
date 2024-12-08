from django.urls import path
from .views import login_view, register, logout_view, terms_and_privacy

urlpatterns = [
    path('login/', login_view, name='login'),  # Ruta del login
    path('register/', register, name='register'),  # Ruta del registro
    path('logout/', logout_view, name='logout'),  # Ruta del logout
    path('terms-and-privacy/', terms_and_privacy, name='terms'),
]