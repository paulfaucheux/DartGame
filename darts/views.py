from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render
from django.views import View
from django.core import serializers

from darts.forms import SubmitPlayerForm, SubmitDart
from darts.models import Player, RefGame, Game, LnkGamePlayer
from darts.utils import getScoreArray, newDartPlayed, cancelLastDart


import numpy as np

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitPlayerForm()
        context = {
            "title": 'New Game'
            , "form": the_form
        }
        return render(request, "darts/home.html", context)
     
    def post(self, request, *args, **kwargs):
        
        the_form = SubmitPlayerForm(request.POST)
        if the_form.is_valid():
            players = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'player7', 'player8']
            
            pk_GameName = the_form.cleaned_data['game']
            obj_refgame = RefGame.objects.get(pk=pk_GameName)
            obj_game = Game.objects.create(GameName=obj_refgame)
            nbPlayer = 0
            
            for player in players: 
                if len(the_form.cleaned_data[player]) > 0:
                    obj_player = Player.objects.get_or_create(PlayerName=the_form.cleaned_data[player])
                    LnkGamePlayer.objects.create(Player=obj_player[0], Game=obj_game)
                    nbPlayer += 1
                    
            obj_game.init()
            obj_player = LnkGamePlayer.objects.filter(Game=obj_game).first()
            #print('the number of player is {0}'.format(nbPlayer))
            if (obj_game is None) | (obj_player is None):
                raise 'There is no Game or no Player'
                
            request.session['pkGame'] = obj_game.pk
            request.session['pkCurrentPlayer'] = obj_player.Player.pk
            request.session['CurrentDart'] = 1
            request.session['CurrentTurn'] = 1
            request.session['nbPlayer'] = nbPlayer

            return HttpResponseRedirect('/game')
        else:
            context = {
                "title": 'New Game'
                , "form": the_form
            }
            return render(request, "darts/home.html", context)

            
            
        
        
class GameView(View):
    def get(self, request, *args, **kwargs):
        the_form_dart = SubmitDart(request.POST)
        obj_game = Game.objects.get(pk=int(request.session['pkGame']))
        
        if obj_game is None:
            raise 'there is no game in the session'
        
        if the_form_dart.is_valid():
            request = newDartPlayed(the_form_dart, request)
        
        context = {
            "title": 'Paie ton Bull'
            , "form_dart": SubmitDart()
            , "table": getScoreArray(obj_game)
            , "current_dart": request.session.get('CurrentDart')
            , "current_turn": request.session.get('CurrentTurn')
            , "player_name": Player.objects.get(pk=int(request.session['pkCurrentPlayer'])).PlayerName
        }
            
        return render(request, "darts/game.html", context)
    
    def post(self, request, *args, **kwargs):
        the_form_dart = SubmitDart(request.POST)
        if the_form_dart.is_valid():
            
            obj_game = Game.objects.get(pk=int(request.session['pkGame']))
            
            if obj_game is None:
                raise 'there is no game in the session'
        
            request = newDartPlayed(the_form_dart, request)
            
            html_score_table = getScoreArray(obj_game)
            the_form_dart = SubmitDart()
            
            context = { "title": 'Paie ton Bull'
                , "table": html_score_table
                , "form_dart": the_form_dart
                , "player_name": Player.objects.get(pk=int(request.session['pkCurrentPlayer'])).PlayerName
                , "current_dart": request.session['CurrentDart']
                , "current_turn": request.session['CurrentTurn']
            }
            
            return render(request, "darts/game.html", context)
            
        else:
            raise 'GameView post() the form received is invalid'
            
            
class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "darts/about.html", {}) 

class ContactView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "darts/contact.html", {})        
        
def cancelLastDart_FV( request, *args, **kwargs):
    obj_game = Game.objects.get(pk=int(request.session['pkGame']))
    
    cancelLastDart(request) # enlever une flechette, et ensuite baisser le score pour chaque joueur
    
    if obj_game is None:
        raise 'there is no game in the session'
        
    context = {
        "title": 'Paie ton Bull'
        , "form_dart": SubmitDart()
        , "table": getScoreArray(obj_game)
        , "current_dart": request.session.get('CurrentDart')
        , "current_turn": request.session.get('CurrentTurn')
        , "player_name": Player.objects.get(pk=int(request.session['pkCurrentPlayer'])).PlayerName
    }

    return render(request, "darts/game.html", context)