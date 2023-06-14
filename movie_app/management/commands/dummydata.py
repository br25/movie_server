from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from movie_app.models import Movie, Review


class Command(BaseCommand):
    help = 'Generate dummy data for movies and reviews'

    def add_arguments(self, parser):
        parser.add_argument('total_movies', type=int, help='Indicates the number of movies to be created')
        parser.add_argument('reviews_per_movie', type=int, help='Indicates the number of reviews per movie')

    def handle(self, *args, **options):
        total_movies = options['total_movies']
        reviews_per_movie = options['reviews_per_movie']

        for _ in range(total_movies):
            name = get_random_string(length=10)
            file_url = 'https://example.com/movie-files/' + get_random_string(length=10)
            image_url = 'https://example.com/movie-images/' + get_random_string(length=10)
            category = get_random_string(length=5)
            rating = round(float(get_random_string(length=1, allowed_chars='0123456789')) + 0.1, 1)

            movie = Movie.objects.create(name=name, file_url=file_url, image_url=image_url,
                                         category=category, rating=rating)

            for _ in range(reviews_per_movie):
                comment = get_random_string(length=20)
                Review.objects.create(comment=comment, movie=movie)

        self.stdout.write(self.style.SUCCESS('Dummy data created successfully!'))
