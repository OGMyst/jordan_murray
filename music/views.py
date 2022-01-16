from django.shortcuts import render

# Create your views here.
def music(request):
    """ A view to return the music page """

    return render(request, 'music/music.html')
