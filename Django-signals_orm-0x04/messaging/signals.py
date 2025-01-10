from .models import Notification, Message
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)