from django.contrib.auth import logout
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse # type: ignore
from .models import Poste
from .forms import RegistrationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Poste, Reaction
from django.core import serializers
from transport.models import Trajet  # type: ignore
from logement.models import Logement  # type: ignore

@csrf_exempt
@require_POST
def add_comment(request):

    if request.user.is_authenticated:
        
        comment_text = request.POST.get('commentText')
        return JsonResponse({'success': True, 'post_id': comment_text}, status=200)

        try:
            post = Poste.objects.get(pk=post_id)
        except Poste.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Post does not exist.'}, status=404)

        # Update the reaction to include the comment
        reaction, created = Reaction.objects.get_or_create(user=request.user, post=post)
        reaction.comment = comment_text
        reaction.save()
        # You can perform additional processing or validation here

        return JsonResponse({'success': True, 'commentId': reaction.id})
    else:
        return JsonResponse({'success': False, 'error': 'User must be authenticated.'}, status=401)

def post_detail(request, pk):
    post = get_object_or_404(Poste, pk=pk)
    return render(request, 'post_detail.html', {'post': post})

@login_required
def notifications(request):
    # Get all posts shared by the current user
    user_posts = Poste.objects.filter(user=request.user)
    # Get all reactions (likes and comments) to these posts
    reactions = Reaction.objects.filter(post__in=user_posts).select_related('user', 'post')

    context = {
        'reactions': reactions,
    }
    return render(request, 'notifications.html', context)


@csrf_exempt
@require_POST
def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Poste, pk=post_id)
        
        # Check if a reaction already exists
        reaction = Reaction.objects.filter(user=request.user, post=post, like=True).first()
        if reaction:
            # If reaction exists, delete it (unlike)
            reaction.delete()
            action = 'unliked'
        else:
            # Otherwise, create a new reaction (like)
            Reaction.objects.create(user=request.user, post=post, like=True)
            action = 'liked'
        
        reaction_count = post.reactions.count()
        return JsonResponse({'success': True, 'reactionCount': reaction_count, 'action': action})
    else:
        return JsonResponse({'success': False, 'error': 'You must be logged in to like posts.'}, status=401)



def get_likers(request, post_id):
    reactions = Reaction.objects.filter(post_id=post_id, like=True)
    likers_list = []

    # Iterate through reactions to get usernames and profile image URLs
    for reaction in reactions:
        user_data = {
            'username': str(reaction.user.username),
            'profile': str(reaction.user.profile.image.url) if hasattr(reaction.user, 'profile') and hasattr(reaction.user.profile, 'image') else None
        }
        likers_list.append(user_data)

    return JsonResponse({'likers': likers_list})
def get_trajet_details(post_id):
    try:
        trajet = Trajet.objects.get(post_id=id)  # Change filter to get and specify the field
    except Trajet.DoesNotExist:
        trajet = None
    return trajet
@login_required
def messagerie(request):
    users = User.objects.all()
    return render(request, 'NewHome.html', {'users': users})
@login_required
def delete_post(request, post_id):
    try:
        post = Poste.objects.filter(id=post_id)
        post.delete()
        return JsonResponse({'success': True})
    except Poste.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Post does not exist'})
@login_required
def index(request):
    return render(request, 'index.html', {'user': request.user})


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    all_posts = Poste.objects.filter(user=user)
    trajets_dict = {trajet.id: trajet for trajet in Trajet.objects.all()}
    logements_dict = {logement.id: logement for logement in Logement.objects.all()}
    
    post_count = Poste.objects.filter(user=user).count()
    like_count = Reaction.objects.filter(user=user, like=True).count()
    comment_count = Reaction.objects.filter(user=user, comment__isnull=False).count()
    
    posts_with_type = []
    for post in all_posts:
        if post.id in trajets_dict:
            posts_with_type.append({'post': post, 'type': 'trajet', 'details': trajets_dict[post.id]})
        elif post.id in logements_dict:
            posts_with_type.append({'post': post, 'type': 'logement', 'details': logements_dict[post.id]})
        else:
            posts_with_type.append({'post': post, 'type': 'other'})

    return render(request, 'mes_postes.html', {
        'user': user,
        'posts_with_type': posts_with_type,
        'post_count': post_count,
        'like_count': like_count,
        'comment_count': comment_count,
    })

@login_required
def acceuil(request):
    all_posts = Poste.objects.all()
    trajets_dict = {trajet.id: trajet for trajet in Trajet.objects.all()}
    logements_dict = {logement.id: logement for logement in Logement.objects.all()}
    
    posts_with_type = []
    for post in all_posts:
        if post.id in trajets_dict:
            posts_with_type.append({'post': post, 'type': 'trajet', 'details': trajets_dict[post.id]})
        elif post.id in logements_dict:
            posts_with_type.append({'post': post, 'type': 'logement', 'details': logements_dict[post.id]})
        else:
            posts_with_type.append({'post': post, 'type': 'other'})

    return render(request, 'acceuil.html', {
        'posts_with_type': posts_with_type,
    })
@login_required
def filter_transport(request):
    all_posts = Poste.objects.all()
    trajets_dict = {trajet.id: trajet for trajet in Trajet.objects.all()}
    posts_with_type = []
    for post in all_posts:
        if post.id in trajets_dict:
            posts_with_type.append({'post': post, 'type': 'trajet', 'details': trajets_dict[post.id]})

    return render(request, 'acceuil.html', {
        'posts_with_type': posts_with_type,
    })
@login_required
def filter_logement(request):
    all_posts = Poste.objects.all()
    logements_dict = {logement.id: logement for logement in Logement.objects.all()}
    posts_with_type = []
    for post in all_posts:
        if post.id in logements_dict:
            posts_with_type.append({'post': post, 'type': 'logement', 'details': logements_dict[post.id]})
    return render(request, 'acceuil.html', {
        'posts_with_type': posts_with_type,
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image')
        description = request.POST.get('description')

        post_type = int(request.POST.get('post_type', 0))  # Providing a default value of 0
        cat_type = int(request.POST.get('cat_type', 2))  # Providing a default value of 2
        
        if cat_type == 0:  # Transport
            destination = request.POST.get('destination')
            nb_places = request.POST.get('nb_places')
            point_depart = request.POST.get('point_depart')
            heure_depart = request.POST.get('heure_depart')
            contactinfo = request.POST.get('contact')
            trajet = Trajet.objects.create(
                user=user,
                image=image,
                description=description,
                cat=cat_type,
                conducteur=user,
                destination=destination,
                point_depart=point_depart,
                heure_depart=heure_depart,
                nb_places=nb_places,
                contactinfo =contactinfo
            )
            return HttpResponse('Trajet created successfully!')

        elif cat_type == 1:  # Logement
            localisation = request.POST.get('localisation')
            
            logement = Logement.objects.create(
                user=user,
                image=image,
                description=description,
                cat=cat_type,
                localisation=localisation
            )
            return HttpResponse('Logement created successfully!')

        else:  # Other categories
            poste = Poste.objects.create(
                user=user,
                image=image,
                description=description,
                cat=cat_type
            )
            return HttpResponse('Post created successfully!')

    return render(request, 'acceuil.html')


@login_required
@login_required
def messagerie(request):
    return render(request,'messages.html')
@login_required
def newPoste(request):
    return render(request,'newPoste.html')
def home(request):
    postes = Poste.objects.all()  # Récupère tous les postes
    return render(request, 'home.html', {'postes': postes})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

def inscrire(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            return render(request, 'register.html', {'form': form})

    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'form': form})
