from django.db import models
from movie_auth.models import User


class FileData(models.Model):
    id = models.IntegerField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    image_url = models.URLField(max_length=255)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.file_name

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ForeignKey(FileData, on_delete=models.CASCADE)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username}: {self.comment}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    files = models.ForeignKey(FileData, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_approve = models.BooleanField(default=False)

    def __str__(self):
        return f"You have received a notification for {self.user.username}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    files = models.ForeignKey(FileData, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return f"Review by {self.user.username} for {self.files.file_name}"
