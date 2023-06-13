from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from movie_app.models import Movie

class Command(BaseCommand):
    help = 'Generates dummy data for the Movie model'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of dummy data to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for _ in range(total):
            name = get_random_string(length=10)
            file_url = get_random_string(length=20)
            image_url = get_random_string(length=20)
            Movie.objects.create(name=name, file_url=file_url, image_url=image_url)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} dummy data.'))
