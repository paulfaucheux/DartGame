import pandas as pd

from django.core import serializers

from darts.models import Game, Player, LnkGamePlayer, LnkGamePlayerScore, LnkGamePlayerDartPlayed, Dart



def getScoreArray(obj_game):
    df_score = pd.DataFrame()
    
    for obj_LnkGamePlayer in LnkGamePlayer.objects.filter(Game=obj_game):
        str_player = obj_LnkGamePlayer.Player
        
        for obj_LnkGamePlayerScore in LnkGamePlayerScore.objects.filter(LnkGamePlayer = obj_LnkGamePlayer):
            int_ScoreValue = obj_LnkGamePlayerScore.ScoreValue
            str_ScoreName = obj_LnkGamePlayerScore.ScoreName
         
            df_score = df_score.append( pd.DataFrame({'Player': str_player, 'Label': str_ScoreName, 'Value': int_ScoreValue} ,index={'index':0}), ignore_index = True)
    
    df_score = df_score.pivot(index='Player', columns='Label', values='Value')
    """
    return df_score.reset_index().to_html(index=False)
    
    """
    df_score_value = df_score.values
    df_score_index = df_score.index
    df_score_columns = df_score.columns

    table = '<th>Player' + '</th><th>'.join(df_score_columns) + '</th>'

    for i in range(0,len(df_score_value)):
        table = table + '<tr><td>' + str(df_score_index[i]) + '</td>'
        for j in range(0,len(df_score_value[i])):
            table = table + '<td>' + str(df_score_value[i][j]) + '</td>'
        table = table + '</tr>'

    return table

            
def getNextPlayerTurn(obj_lnkgameplayer):
    return (obj_lnkgameplayer.Player, 2)

def newDartPlayed(the_form_dart, request):
    obj_game = Game.objects.get(pk=int(request.session['pkGame']))
    current_player = Player.objects.get(pk=int(request.session['pkCurrentPlayer']))
    current_dart = request.session['CurrentDart']
    
    obj_lnkgameplayer = LnkGamePlayer.objects.get(Game=obj_game, Player=current_player)
    
    print('Dart info type: {0}, value:{1}'.format(type(the_form_dart.cleaned_data['dart1']),the_form_dart.cleaned_data['dart1']))
    obj_dartplayed = LnkGamePlayerDartPlayed.objects.create(
        LnkGamePlayer=obj_lnkgameplayer
        , Dart = Dart.objects.get(DartName=str(the_form_dart.cleaned_data['dart1']))
        , Turn = current_dart
    )

    current_player, current_dart = getNextPlayerTurn(obj_lnkgameplayer)
    
    request.session['CurrentPlayer'] = current_player.pk
    request.session['CurrentDart'] = current_dart

    return request
