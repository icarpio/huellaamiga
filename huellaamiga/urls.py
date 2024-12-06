from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView  # Para redirecciones


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('home/', include('home.urls')),  # Incluye las URLs de la app home
    path('huellapp/', include('huellapp.urls')),  # Incluye las URLs de la app posts
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),  # Redirige la raíz al login
]