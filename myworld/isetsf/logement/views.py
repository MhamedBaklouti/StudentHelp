from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import LogementForm
from .models import Logement
from django.urls import reverse
from django.http import JsonResponse,HttpResponseForbidden,HttpResponseNotAllowed

@login_required
def liste_logement(request):
    # Retrieve all logements
    logements = Logement.objects.all()

    for logement in logements:
        if hasattr(logement.user, 'profile') and logement.user.profile.image:
            logement.profile_image = logement.user.profile.image.url
            logement.profile_name = logement.user.username
        else:
            logement.profile_image = None

    # Add a check for valid ID
    if not logement.id:
        # Handle the case where the ID is missing
        # You can log an error or set a default ID
        logement.id = 0  # Example: Set a default ID

    return render(request, 'logement.html', {'liste': logements})


@login_required
def delete_logement(request, logementId):
    # Get the logement object by its ID
    logement = get_object_or_404(Logement, pk=logementId)
    # Check if the request method is POST
    if request.method == 'POST':
        # Check if the logged-in user has permission to delete the logement
        if request.user == logement.user:  # Assuming each logement has a 'user' field
            # Delete the logement
            logement.delete()
            # Redirect to some other page or return a success message
            return redirect('liste_logement')  # Change 'some_redirect_url' to the desired URL
        else:
            # If the user does not have permission, return a forbidden response
            return HttpResponseForbidden("You do not have permission to delete this logement.")

    # If the request method is not POST, return a method not allowed response
    return HttpResponseNotAllowed(['POST'])
    
@login_required
def mes_logement_posts(request):
    posts = Logement.objects.filter(user_id = request.user.id)
    for post in posts:
        post.profile_image = post.user.profile.image.url if post.user.profile.image else None
    return render(request,'mes_logement_posts.html',{'posts':posts})

@login_required
def add_logement(request):
    if request.method == 'POST':
        form = LogementForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('liste_logement')
    else:
        if not request.user.is_authenticated:
            return redirect(reverse('login_view'))
        form = LogementForm()
    return render(request, 'addlogement.html', {'form': form})


@login_required
def edit_logement(request, logement_id):
    logement = get_object_or_404(Logement, id=logement_id)
    if request.method == 'POST':
        form = LogementForm(request.POST, instance=logement)
        # Extract the specific fields from the form data
        localisation = request.POST.get('localisation')
        description = request.POST.get('description')
        
        # Update the Logement instance with the specific fields
        logement.localisation = localisation
        logement.description = description
        logement.save(update_fields=['localisation', 'description'])
        return JsonResponse({'message': 'Logement edited successfully'})

    return redirect('liste_logement')
