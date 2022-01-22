from django.shortcuts import render
from .models import GenreInfo
# Create your views here.
def music(request):
    """ A view to return the music page """

    genres = GenreInfo.objects.all().order_by('title')
    context ={
        'genres': genres
    }

    return render(request, 'music/music.html', context)
