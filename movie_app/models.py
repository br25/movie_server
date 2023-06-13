from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    file_url = models.URLField()
    image_url = models.URLField()

    def __str__(self):
        return self.name
