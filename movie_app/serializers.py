from rest_framework import serializers
from .models import Movie, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'comment', 'created_at', 'movie']

class MovieSerializer(serializers.ModelSerializer):
   class Meta:
        model = Movie
        fields = ['id', 'name', 'file_url', 'image_url', 'category', 'rating']
