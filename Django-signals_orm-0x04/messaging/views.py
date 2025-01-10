from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Message


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