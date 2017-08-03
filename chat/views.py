from django.shortcuts import render, redirect
from .models import Room
import haikunator
from django.db import transaction
import random
import string
from django.core.exceptions import ObjectDoesNotExist

def new_room(request):
    """
    Randomly create a new room, and redirect to it.
    """
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)
    return redirect(chat_room, label=label)

def chat_room(request):
    """
    Room view - show the room, with latest messages.
    The template for this view has the WebSocket business to send and stream
    messages, so see the template for where the magic happens.
    """
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    # try:
    #     room = Room.objects.get(label=label)
    # except ObjectDoesNotExist:
    #     return render(label);

    room, created = Room.objects.get_or_create(label='questions')

    #if(created):
    #    return render(label);

    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    if request.user.is_superuser:
        return render(request, "chat/room_professor.html", {
            'room': room,
            'messages': messages,
            'messagecount': getMessageCount(),
        })
    else:
        return render(request, "chat/room.html", {
            'room': room,
            'messages': messages,
            'messagecount': getMessageCount(),
        })


def getMessageCount():
    room, created = Room.objects.get_or_create(label='questions')
    return room.messages.count()