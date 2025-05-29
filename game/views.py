from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from . models import Game
from . forms import TryForm


def index(request):
	current_game = None
	total_games = 0

	if request.user.is_authenticated:
		game = Game.objects.filter(user = request.user).order_by("id").last()
		current_game = game if game and not game.is_completed else None

		games = Game.objects.filter(user = request.user)
		total_games = games.count()
		total_tries = sum(game.tries.count() for game in games)
		if current_game:
			total_games -= 1
			total_tries -= current_game.tries.count()

	return render(
		request,
		'game/index.html',
		{
			'current_game': current_game,
			'total_games': total_games
		},
	)

@login_required
def start_a_new_game(request):
	game = Game.create_a_new_game(request.user)
	return redirect('play_game')


@login_required
def play_a_game(request):
	game = Game.objects.filter(user=request.user).first()

	form = TryForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		guess = form.cleaned_data['guess']
		Game.make_a_turn(game, guess)
		return redirect('play_game')

	tries = game.tries.order_by('-created_at')

	return render(
		request, 'game/play_game.html', {'game': game, 'form': form, 'tries': tries}
	)