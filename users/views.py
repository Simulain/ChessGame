from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from chess.models import COMPLETED, Game
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}! Log in now!')
            form.save()
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    games = []
    all = Game.objects.filter(Q(host=request.user) | Q(opponent=request.user)).filter(status=COMPLETED).order_by('-id')
    for game in all:
        game_info = {}

        game_info['game'] = game
        game_info['link'] = f"/multi/{game.id}"
        game_info['side'] = determine_side(game, request.user)

        game_info['opponent'] = game.opponent
        if game.host != request.user:
            game_info['opponent'] = game.host

        game_info['result_text'] = "You Won!"
        if game.winner != request.user:
            game_info['result_text'] = "You Lost!"

        games.append(game_info)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'games' : games
    }
    return render(request, 'users/profile.html', context)

def test(request):
    return render(request, 'users/test.html')


# Helper functions
def determine_side(game, user):
    if user == game.host:
        if game.host_white:
            return 'White'
        else:
            return 'Black'
    else:
        if game.host_white:
            return 'Black'
        else:
            return 'White'
