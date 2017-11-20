from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render
from django.views import View
from darts.forms import SubmitPlayerForm

from darts.models import Player

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
        context = {
            "form": the_form
        }
        template = "darts/home.html"
        if the_form.is_valid():
            players = np.array(the_form.cleaned_data.get("player1"))
            players.append(the_form.cleaned_data.get("player2"))
            """
            players.append(the_form.cleaned_data.get("player3"))
            players.append(the_form.cleaned_data.get("player4"))
            players.append(the_form.cleaned_data.get("player5"))
            players.append(the_form.cleaned_data.get("player6"))
            players.append(the_form.cleaned_data.get("player7"))
            players.append(the_form.cleaned_data.get("player8"))
            """
            
            NumberOfPlayer = 0
            obj_players = []
            
            for player in players: 
                if player is not None:
                    NumberOfPlayer += 1
                    obj_player, created = Player.objects.get_or_create(PlayerName=player)
                    obj_players = np.append(obj_player)
                    obj_game = RefGame.objects.get_or_create(RefGame=)

                
            
            

            # ON CREE un PlayerScore
            
            
            template = "darts/game.html"
            
        return render(request, template, context)

 
