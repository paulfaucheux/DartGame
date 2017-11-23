from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render
from django.views import View
from django.core import serializers

from darts.forms import SubmitPlayerForm, SubmitDart
from darts.models import Player, RefGame, Game, LnkGamePlayer
from darts.utils import getScoreArray, newDartPlayed

import numpy as np

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitPlayerForm()
        context = {
            "title": 'Paie ton Bull'
            , "form": the_form
        }
        return render(request, "darts/home.html", context)
     
    def post(self, request, *args, **kwargs):
        the_form = SubmitPlayerForm(request.POST)
        if the_form.is_valid():
            players = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'player7', 'player8']
            players = ['player1', 'player2']  

            obj_refgame = RefGame.objects.get(GameName='Cricket')
            obj_game = Game.objects.create(GameName=obj_refgame)
            
            for player in players: 
                if the_form[player] is not None:
                    obj_player = Player.objects.get_or_create(PlayerName=the_form.cleaned_data[player])
                    LnkGamePlayer.objects.create(Player=obj_player[0], Game=obj_game)
                    
            obj_game.init()
            obj_player = LnkGamePlayer.objects.filter(Game=obj_game).first()
            
            request.session['pkGame'] = obj_game.pk
            request.session['pkCurrentPlayer'] = obj_player.Player.pk
            request.session['CurrentDart'] = 1
            
        else:
            raise 'The form sent from darts/home.html is not valid initialisation impossible'
            
        return HttpResponseRedirect('./game')
        
class GameView(View):
    def get(self, request, *args, **kwargs):
        the_form_dart = SubmitDart(request.POST)
        
        if 'Game' in request.session:
            obj_game = Game.objects.get(pk=int(request.session['pkGame']))
        else:
            return HttpResponseRedirect('./home')
        
        if the_form_dart.is_valid():
            current_player, current_dart = newDartPlayed(the_form_dart, request)
                
        context = {
            "title": 'Paie ton Bull'
            , "form_dart": SubmitDart()
            , "table": getScoreArray(obj_game)
            , "current_dart": request.COOKIES.get('CurrentDart')
        }
            
        return render(request, "darts/game.html", context)
    
    def post(self, request, *args, **kwargs):
        the_form_dart = SubmitDart(request.POST)
        if the_form_dart.is_valid():
            
            obj_game = Game.objects.get(pk=int(request.session['pkGame']))
            request = newDartPlayed(the_form_dart, request)
        
            html_score_table = getScoreArray(obj_game)
            the_form_dart = SubmitDart()
    
            context = { "title": 'Paie ton Bull'
                , "table": html_score_table
                , "form_dart": the_form_dart
                , "player_name": Player.objects.get(pk=int(request.session['pkCurrentPlayer'])).PlayerName
                , "current_dart": request.session['CurrentDart']
            }
    
        else:
            'GameView post() the form received is invalid'
            
        return render(request, "darts/game.html", context)
