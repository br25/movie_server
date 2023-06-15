from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, Notification

@receiver(post_save, sender=Comment)
def create_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        comment = instance
        message = "Please approve my comment."
        files = instance.files  # Replace this with the actual files object or its primary key
        Notification.objects.create(user=user, comment=comment, files=files, message=message)
