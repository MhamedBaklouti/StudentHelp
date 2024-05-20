from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('study.urls')),
    path('', include('chat.urls')),
    path('',include('transport.urls')),
    path('',include('logement.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
