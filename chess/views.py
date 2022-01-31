from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Game

def chessGame(request):
    return render(request, 'chess/game.html')


class create(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'chess/create.html')

    def post(self, request):
        userstring = request.POST["username"]
        side = request.POST["side"].lower()
        try:
            host_white = True
            if side != 'white':
                host_white = False

            opp = User.objects.get(username=userstring)
            game = Game(host=request.user, opponent=opp, host_white=host_white)
            game.save()

            return HttpResponseRedirect('/multi/' + str(game.pk))
        except:
            messages.error(request, f'The user could not be found! Try again.')
            return render(request, 'chess/create.html')


def multiplayer(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    return render(request, 'chess/multiplayer.html', {"game_id" : game_id})


def home(request):
    return render(request, 'chess/home.html')

def about(request):
    return render(request, 'chess/home.html')
