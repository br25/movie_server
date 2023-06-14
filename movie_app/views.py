from django.views.generic import ListView, DetailView
from .models import Movie

class MovieListView(ListView):
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies'


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
