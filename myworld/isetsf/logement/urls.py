
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from . import views
from django.urls import path
urlpatterns = [

    path('logement',views.liste_logement,name='liste_logement'),
    path('delete_logement/<int:logementId>', views.delete_logement, name='delete_logement'),
    path('mes_logement_posts',views.mes_logement_posts,name='mes_logement_posts'),
    path('addlogement',views.add_logement,name='add_logement'),
    path('edit_logement/<int:logement_id>', views.edit_logement, name='edit_logement'),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    