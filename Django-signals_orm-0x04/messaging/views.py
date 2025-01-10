from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Message


def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return HttpResponse('Account deleted successfully.')


def threaded_conversations(request):
    messages = Message.objects.select_related('sender', 'receiver').prefetch_related('replies').filter(parent_message=None)
    return render(request, 'threaded_conversations.html', {'messages': messages})
