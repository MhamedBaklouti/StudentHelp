
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [

    path('inscrire', views.inscrire, name='inscrire'),
    path('',views.login_view,name='login_view'),
    path('index',views.index,name='index'),
    path('logout',views.logout_view,name='logout'),
    # path('mes_postes',views.mes_postes,name='mes_postes'),
    path('newPoste',views.newPoste,name='newPoste'),
    path('create_post', views.create_post, name='create_post'),
    path('admin/', admin.site.urls),
    path('acceuil', views.acceuil, name='acceuil'),
    path('filter_transport', views.filter_transport, name='filter_transport'),
    path('filter_logement', views.filter_logement, name='filter_logement'),
    path('chating', views.messagerie, name='messagerie'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('get_likers/<int:post_id>/', views.get_likers, name='get_likers'),
    path('get_trajet_details/<int:post_id>/', views.get_trajet_details, name='get_trajet_details'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('notifications/', views.notifications, name='notifications'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('profile/<int:id>/', views.user_profile, name='user_profile'),


  


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

