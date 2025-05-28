from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib import admin

# Create your models here.

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.PositiveIntegerField("Number", validators = [ MinValueValidator(1), MaxValueValidator(10) ])
    created_at = models.DateTimeField("Creation Data", auto_now_add = True)

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
    guess = models.PositiveIntegerField("Turn", validators = [ MinValueValidator(1), MaxValueValidator(10) ])
    created_at = models.DateTimeField("Creation Data", auto_now_add = True)