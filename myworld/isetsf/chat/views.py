from django.shortcuts import render, redirect
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

# Create your views here.
@login_required
def home(request):
    current_user = request.user
    users = User.objects.exclude(id=current_user.id).exclude(is_superuser=True)
    return render(request, 'NewHome.html', {'users': users})
@login_required
def room(request, room):
    username = request.user.username
    users = User.objects.exclude(id=request.user.id).exclude(is_superuser=True)
    room_details = Room.objects.get(name=room)
    return render(request, 'NewHome.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'users':users
    })
@login_required
def checkview(request):
    if request.method == 'POST':
        user2 = request.POST.get('clicked_username')  # Retrieve clicked username from POST data
        if user2:
            room = ''.join(sorted([request.user.username, user2]))
            username = request.user.username

            if Room.objects.filter(name=room).exists():
                return redirect('/'+room+'/?username='+username)
            else:
                new_room = Room.objects.create(name=room)
                new_room.save()
                return redirect('/'+room+'/?username='+username)
        else:
            # Handle the case where no username was clicked
            return HttpResponse("No username selected")
    else:
        # Handle the case where the request method is not POST
        return HttpResponse("Invalid request method")

def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})