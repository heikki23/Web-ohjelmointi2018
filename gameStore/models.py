from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
MAX_JSON_DATA_LEN = 2048


class Game(models.Model):
    game_url = models.URLField(max_length = 200, unique = True, default = '')
    name = models.CharField(max_length = 225, unique = True)
    description = models.TextField()
    price = models.DecimalField(max_digits = 5,decimal_places=2)
    price_currency = models.CharField(max_length = 3, default = '€')
    developer_name = models.CharField(default = 'UNKNOWN', max_length=225)

    def to_dict(self):
        data = {}
        data['name'] = self.name
        return data

#We are using custom user model, so we must create own UserManager too
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            #NOTE: This is set to True, so people can create new
            is_active = True
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length = 225, unique = True)
    # isDeveloper and isPlayer are Booleanfiels, which tells is the user developer ore the player
    isDeveloper = models.BooleanField(default=False)
    isPlayer = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='email address',
        max_length=255)
    games = models.ManyToManyField(Game,related_name = "games")
    shopcartGames = models.ManyToManyField(Game,related_name = "shopcartGames")
    emailConfirmed = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.username

    #must do own emai_user function, when using custon user model.
    def email_user(self, subject, message, from_email = None, **kwargs):
        send_mail(subject,message,from_email,[self.email],**kwargs)

class SalesManager(models.Manager):
    def create_sales(self,player,game):
        sale = self.create(player=player, totPrice = game.price)
        sale.games.add(game)
        return sale

class Sales(models.Model):
    player = models.ForeignKey(User,related_name = "salesPlayer", on_delete=models.CASCADE, null = True)
    games = models.ManyToManyField(Game,related_name = "salesGame", blank = True)
    date = models.DateTimeField(default = timezone.now)
    totPrice = models.DecimalField(max_digits = 5,decimal_places=2)
    status = models.CharField(max_length = 225, null = False, default = "pending")

    objects = SalesManager()

class GameState(models.Model):
    gameState = models.CharField(max_length=MAX_JSON_DATA_LEN)
    game = models.ForeignKey(Game,related_name = "game_save", on_delete=models.CASCADE)
    player = models.ForeignKey(User,related_name = "player", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("game","player"),)

class GameScore(models.Model):
    score = models.FloatField(default=0)
    game = models.ForeignKey(Game,related_name = "game_score", on_delete=models.CASCADE)
    player = models.ForeignKey(User,related_name = "player_score", on_delete=models.CASCADE)
