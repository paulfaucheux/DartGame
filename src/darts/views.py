from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render
from django.views import View
from darts.forms import SubmitPlayerForm

from darts.models import Player, RefGame, Game, LnkGamePlayer
from darts.utils import getScoreArray

import numpy as np

# Create your views here.

class HomeView(View):
    def get(self, request, *args, **kwargs):
        the_form = SubmitPlayerForm()
        context = {
            "form": the_form
        }
        return render(request, "darts/home.html", context)
     
    def post(self, request, *args, **kwargs):
        the_form = SubmitPlayerForm(request.POST)
        template = "darts/game.html"
        if the_form.is_valid():
            players = np.array(the_form.cleaned_data.get("player1"))
            players = np.append(players, the_form.cleaned_data.get("player2"))
            """
            players.append(the_form.cleaned_data.get("player3"))
            players.append(the_form.cleaned_data.get("player4"))
            players.append(the_form.cleaned_data.get("player5"))
            players.append(the_form.cleaned_data.get("player6"))
            players.append(the_form.cleaned_data.get("player7"))
            players.append(the_form.cleaned_data.get("player8"))
            """
            
            NumberOfPlayer = len(players)
            obj_players = []
            obj_refgame = RefGame.objects.get(GameName='Cricket')
            obj_game = Game.objects.create(GameName=obj_refgame)
            
            for player in players: 
                if player is not None:
                    obj_player, created = Player.objects.get_or_create(PlayerName=player)
                    gamePlayer = LnkGamePlayer.objects.create(Player=obj_player, Game=obj_game)
                    
            
            obj_game.init()
            
            html_score_table = getScoreArray(obj_game)
            context = {
                "table": html_score_table
            }
            return render(request, template, context)
        else:
            context = {
                "error": 'The form sent from darts/home.html is not valid initialisation impossible'
            }
            return render(request, "darts/error.html", context)
        
                    
                    
                    

                
            
            

            # ON CREE un PlayerScore
            
            
            template = "darts/game.html"
            
        return render(request, template, context)

 
