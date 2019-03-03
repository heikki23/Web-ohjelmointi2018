from django.test import TestCase, Client
from django.db import models
from django.template.loader import render_to_string
from django.http import HttpRequest
import random, string, unittest
from . models import User, UserManager, Game
# Create your tests here.

class SimpleTest(TestCase):


    def SetUp(self):
        self.client = Client()
        self.randstr = ''.join(random.sample(string.ascii_letters, 5))
        self.randint = random.randint(5,50)
        user = User.objects.create_user(username = 'testikayttaja',email = 'testi@gmail.com', password = 'testi')

    def test_gamestore(self):
        response = self.client.get('/gamestore/')
        self.assertEqual(response.status_code, 200, "Testing that a request to /gamestore/ succeeded")

    def test_not_logged(self):
        response = self.client.get('/gamestore/your_games')
        self.assertRedirects(response,'/gamestore/login?next=/gamestore/your_games')

    def test_login_and_logout(self):
        #create new use
        user = User.objects.create_user(username = 'testikayttaja',email = 'testi@gmail.com', password = 'testi')
        #try login
        response = self.client.post('/gamestore/login',{'username': 'testikayttaja','password': 'testi'}, follow = True)
        self.assertTrue(response.context['user'].is_active, "Testing that login works")
        response = self.client.logout()
        response = self.client.get('/gamestore/your_games')
        self.assertRedirects(response,'/gamestore/login?next=/gamestore/your_games')

    # def test_play_game(self):
    #     user = User.objects.create_user(username = 'testikayttaja',email = 'testi@gmail.com', password = 'testi')
    #     response = self.client.post('/gamestore/login',{'username': 'testikayttaja','password': 'testi'}, follow = True)
    #     self.assertTrue(response.context['user'].is_active, "Testing that login works")
    #     #Add game to the user, and check that there is is_authenticated
    #     game = Game.objects.create( game_url = "https://cdn.rawgit.com/piehei/4e5efb4941887a7dab3cd2f036b0b9eb/raw/af781b523f05b746ef1020e68b4bba9501e86b71/example_game.html", name = "test", description = "test", price = 5)
    #     response.context['user'].games.add(game)
    #     self.assertEqual(response.context['user'].games.get(name = game.name).name, game.name)
    #     #print(game.pk)
    #     #response = self.client.get('/gamestore/game_window/2')
    #     #self.assertEqual(response.status_code, 200, "Testing that a request to game_window succeeded")
