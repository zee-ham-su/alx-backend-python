from .models import Notification, Message, MessageHistory
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Check if the message already exists (is not new)
        try:
            original = Message.objects.get(pk=instance.pk)
            if original.content != instance.content:  # Check if content has been edited
                # Save old content to MessageHistory
                MessageHistory.objects.create(message=original, old_content=original.content)
                instance.edited = True  # Mark the message as edited
        except Message.DoesNotExist:
            pass