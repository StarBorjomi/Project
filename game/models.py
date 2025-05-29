from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib import admin

import random

# Create your models here.

class Game(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	number = models.PositiveIntegerField("Number", validators = [ MinValueValidator(1), MaxValueValidator(100) ])
	created_at = models.DateTimeField("Creation Data", auto_now_add = True)

	@staticmethod
	def generate_number():
		return random.randint(1, 100)

	@staticmethod
	def evaluate_guess(number, guess):
		if guess == number:
			return '='
		return '>' if guess > number else '<'

	@staticmethod
	def create_a_new_game(user):
		number = Game.generate_number()
		return Game.objects.create(user = user, number = number)

	@staticmethod
	def make_a_turn(game, guess):
		guess = int(guess)
		response = Game.evaluate_guess(game.number, guess)
		return Try.objects.create(game = game, response = response, guess = guess)

	@property
	@admin.display(boolean = True, description = "Comlpeted")
	def is_completed(self):
		return self.tries.filter(guess=self.number).exists()
	
	@property
	@admin.display(boolean = True, description = "Tries")
	def number_of_tries(self):
		return self.tries.count()

class Try(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="tries")
	guess = models.PositiveIntegerField("Turn", validators = [ MinValueValidator(1), MaxValueValidator(100) ])
	response = models.CharField("Response", validators = [ MaxValueValidator(1) ], default='o')
	created_at = models.DateTimeField("Creation Data", auto_now_add = True)