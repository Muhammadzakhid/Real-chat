from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages as django_messages
from django.views.decorators.csrf import csrf_exempt

from chat.models import UserRelation, Messages
from chat.serializers import MessageSerializer


# Create your views here.

@login_required(login_url='login')
def chat(request, username):
    try:
        usersen = request.user
        friend = User.objects.get(username=username)
        exists = UserRelation.objects.filter(
            user=request.user, friend=friend, accepted=True
        ).exists()

        if not exists:
            django_messages.error(
                request, "You are not able to chat with this user"
            )  # User the renamed variable here
            return redirect('home')
    except User.DoesNotExists:
        return redirect("home")

    messages = Messages.objects.filter(
        sender_name=usersen, receiver_name=friend
    ) | Messages.objects.filter(sender_name=friend, receiver_name=usersen)
    if request.method == 'GET':
        return render(
            request,
            'chat.html',
            {
                'messages': messages,
                'curr_user': usersen,
                'friend': friend,
            },
        )


@login_required(login_url="login")
@csrf_exempt
def message_list(request, sender=None, receiver=None):
    if request.method == "GET":
        messages = Messages.objects.filter(
            sender_name=sender, receiver_name=receiver, seen=False
        )
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )