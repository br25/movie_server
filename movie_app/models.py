from django.db import models
from movie_auth.models import User
from django.db.models import Avg


class FileData(models.Model):
    file_name = models.CharField(max_length=255)
    file_url = models.URLField(max_length=255)
    image_url = models.URLField(max_length=255)
    category = models.CharField(max_length=255)
    year = models.CharField(max_length=255)

    def __str__(self):
        return self.file_name

    def get_average_rating(self):
        return self.file_ratings.aggregate(average_rating=Avg('rating'))['average_rating']


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_data = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='file_comments')
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment by {self.user.username}: {self.comment}"


class Ratings(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_data = models.ForeignKey(FileData, on_delete=models.CASCADE, related_name='file_ratings')
    rating = models.IntegerField(choices=RATING_CHOICES)
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return f"Review by {self.user.username} for {self.file_data.file_name}"

    def save(self, *args, **kwargs):
        skip_update = kwargs.pop('skip_update', False)
        super().save(*args, **kwargs)
        if not skip_update:
            self.update_average_rating()
    

    def update_average_rating(self):
        average_rating = Ratings.objects.filter(file_data=self.file_data).aggregate(avg_rating=Avg('rating'))['avg_rating']
        self.average_rating = average_rating
        self.save(update_fields=['average_rating'], skip_update=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE)
    file_data = models.ForeignKey(FileData, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification from {self.user.username}, file name: {self.file_data.file_name}, file ID: {self.file_data.id}, and comment is: {self.comment.comment}. Is approved? {self.is_approved}"
