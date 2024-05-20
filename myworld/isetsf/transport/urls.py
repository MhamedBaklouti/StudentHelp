
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views
from django.urls import path
urlpatterns = [
    path('custom_denied_page', views.custom_denied_view, name='custom_denied_page'),
    path('mes_transport_postes', views.mes_transport_postes, name='mes_transport_postes'),
    path('covoiturage',views.liste_covoiturage,name='liste_covoiturage'),
    path('addcovoiturage',views.add_covoiturage,name='add_covoiturage'),
    path('edit-trajet/<int:trajet_id>', views.edit_trajet, name='edit_trajet'),
    path('delete-trajet/<int:trajet_id>/', views.delete_trajet, name='delete_trajet'),
    # Other URL patterns
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    