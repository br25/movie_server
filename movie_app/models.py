from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    file_url = models.URLField()
    image_url = models.URLField()
    category = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.name


class Review(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.comment
