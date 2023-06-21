from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comments, Notification

@receiver(post_save, sender=Comments)
def create_notification(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        comment = instance
        file_data = instance.file_data
        Notification.objects.create(user=user, comment=comment, file_data=file_data)
