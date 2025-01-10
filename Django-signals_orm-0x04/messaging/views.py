from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponse('Account deleted successfully.')


def threaded_conversations(request):
    # Fetch root messages (those without a parent) and optimize queries
    root_messages = Message.objects.filter(parent_message=None).select_related('sender', 'receiver').prefetch_related('replies')
    
    # Prepare messages with their threaded replies
    threaded_data = []
    for message in root_messages:
        threaded_data.append({
            'message': message,
            'replies': message.get_threaded_replies()
        })

    return render(request, 'threaded_conversations.html', {'messages': threaded_data})

@cache_page(60)  # Cache the view for 60 seconds
@login_required
def threaded_conversations(request):
    # Fetch root messages (those without a parent) involving the logged-in user
    root_messages = Message.objects.filter(
        parent_message=None
    ).filter(
        sender=request.user  # Messages sent by the user
    ).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        'replies__sender', 'replies__receiver'
    )

    # Prepare messages with their threaded replies
    threaded_data = []
    for message in root_messages:
        threaded_data.append({
            'message': message,
            'replies': message.get_threaded_replies()
        })

    return render(request, 'threaded_conversations.html', {'messages': threaded_data})

@login_required
def unread_messages(request):
    # Fetch unread messages for the logged-in user
    unread_messages = Message.unread.unread_for_user(request.user).only(sender='sender', content='content', timestamp='timestamp')

    return render(request, 'unread_messages.html', {'messages': unread_messages})
