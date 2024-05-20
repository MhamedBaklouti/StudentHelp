from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TrajetForm
from .models import Trajet
from django.http import JsonResponse



@login_required
def edit_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    return JsonResponse({'message': request.POST.get('description')})

    if request.method == 'POST':
        # Extract the specific fields from the form data
        destination = request.POST.get('destination')
        point_depart = request.POST.get('point_depart')
        heure_depart = request.POST.get('heure_depart')
        nb_places = request.POST.get('nb_places')

        # Update the Logement instance with the specific fields
        trajet.destination = destination
        trajet.point_depart = point_depart
        trajet.heure_depart = heure_depart
        trajet.nb_places = nb_places
        trajet.save(update_fields=['destination', 'point_depart','heure_depart','nb_places'])
        return JsonResponse({'message': 'Trajet edited successfully'})

    return redirect('liste_covoiturage')

def delete_trajet(request, trajet_id):
    trajet = get_object_or_404(Trajet, id=trajet_id)
    trajet.delete()
    return JsonResponse({'success': True})

def custom_denied_view(request):
    return render(request, 'denied.html')

def liste_covoiturage(request):
    covoiturages = Trajet.objects.all()
    for covoiturage in covoiturages:
        if hasattr(covoiturage.user, 'profile') and covoiturage.user.profile.image:
            covoiturage.profile_image = covoiturage.user.profile.image.url
            covoiturage.profile_name = covoiturage.user.username
        else:
            covoiturage.profile_image = None
    return render(request,'covoiturage.html',{'liste':covoiturages})

@login_required
def mes_transport_postes(request):
    postes = Trajet.objects.filter(conducteur_id = request.user.id)
    return render(request,'mes_transport_postes.html',{'postes':postes})

@login_required
def add_covoiturage(request):
    if request.method == 'POST':
        form = TrajetForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.conducteur = form.user = request.user
            form.save()
            return redirect('liste_covoiturage')
    else:
        if not request.user.is_authenticated:
            return redirect(reverse('login_view'))  # Redirect to the LOGIN_URL
        form = TrajetForm()
    return render(request, 'addcovoiturage.html', {'form': form})
