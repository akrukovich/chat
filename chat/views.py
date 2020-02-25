import random
from django.db import transaction
from django.shortcuts import render, redirect
from .models import ChatRoom, Message
from django.views.generic import DetailView
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger

def about(request):
    return render(request, "chat/about.html")


def new_room(request):
    new_room = None
    while not new_room:
        with transaction.atomic():
            label = ''.join(['Chat', str(random.randint(1, 100))])
            if ChatRoom.objects.filter(label=label).exists():
                continue
            new_room = ChatRoom.objects.create(label=label)
    return redirect(chat_room, label=label)


def chat_room(request, label):
    room, created = ChatRoom.objects.get_or_create(label=label)

    messages = room.messages.order_by('-timestamp').all()
    paginator = Paginator(messages, 5)
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        messages = paginator.page(paginator.num_pages)

    return render(request, "chat/room.html", {
        'room': room,
        'messages': messages,
    })
class MessageDetailView(DetailView):
    model = Message