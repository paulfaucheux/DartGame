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

    table = '<thead><tr><th>Player</th><th>' + '</th><th>'.join(df_score_columns) + '</th></tr></thead><tbody>'

    for i in range(0,len(df_score_value)):
        table = table + '<tr><td>' + str(df_score_index[i]) + '</td>'
        for j in range(0,len(df_score_value[i])):
            table = table + '<td>' + str(df_score_value[i][j]) + '</td>'
        table = table + '</tr>'
    table = table + '</tbody>'
    return table

def updateScoreOtherPlayersCricket(dart, extra_score, obj_game, current_player):
    players_score = LnkGamePlayerScore.objects.filter(LnkGamePlayer__in= LnkGamePlayer.objects.filter(Game=obj_game), ScoreName = dart.ValueDart)
    for player in players_score:
        if player.ScoreValue < 3:
            main_player_score = LnkGamePlayerScore.objects.get(LnkGamePlayer = player.LnkGamePlayer, ScoreName='Score')
            main_player_score.ScoreValue += int(dart.ValueDart) * extra_score
            main_player_score.save()

def updateScoreCurrentPlayerCricket(lnkGamePlayer, score):
    main_player_score = LnkGamePlayerScore.objects.get(LnkGamePlayer = lnkGamePlayer, ScoreName='Score')
    main_player_score.ScoreValue += score
    main_player_score.save()

def updateScoreCurrentPlayer(obj_DartPlayed):

    obj_game = Game.objects.get(pk=obj_DartPlayed.LnkGamePlayer.Game.pk)
    dart = Dart.objects.get(pk=obj_DartPlayed.Dart.pk)
    current_scores = LnkGamePlayerScore.objects.filter(LnkGamePlayer=obj_DartPlayed.LnkGamePlayer)
    
    if obj_game.GameName.GameName == 'Cricket - Cut the throat':
        for score in current_scores:
            if score.ScoreName == dart.ValueDart:
                score.ScoreValue += dart.TimeValue
                score.save()
                if score.ScoreValue > 3:
                    extra_score = score.ScoreValue - 3
                    score.ScoreValue = 3
                    score.save()
                    updateScoreOtherPlayersCricket(dart, extra_score, obj_game, obj_DartPlayed.LnkGamePlayer.Player)
    elif obj_game.GameName.GameName == 'Cricket - Standard':
        for score in current_scores:
            if score.ScoreName == dart.ValueDart:
                score.ScoreValue += dart.TimeValue
                score.save()
                if score.ScoreValue > 3:
                    extra_score = score.ScoreValue - 3
                    score.ScoreValue = 3
                    score.save()
                    updateScoreCurrentPlayerCricket(obj_DartPlayed.LnkGamePlayer, int(dart.ValueDart) * extra_score)
    else:
        raise 'No rules to update the score for game {0}'.format(obj_game.GameName.GameName)
    
        
    

def newDartPlayed(the_form_dart, request):
    

    
    obj_game = Game.objects.get(pk=int(request.session['pkGame']))
    current_player = Player.objects.get(pk=int(request.session['pkCurrentPlayer']))
    current_dart = request.session['CurrentDart']
    
    
    obj_lnkgameplayer = LnkGamePlayer.objects.get(Game=obj_game, Player=current_player)

    obj_DartPlayed = LnkGamePlayerDartPlayed.objects.create(
        LnkGamePlayer=obj_lnkgameplayer
        , Dart = Dart.objects.get(DartName=str(the_form_dart.cleaned_data['dart1']))
        , Turn = current_dart
    )
    
    updateScoreCurrentPlayer(obj_DartPlayed)
    
    current_dart += 1
    
    
    if current_dart >= 4:
        current_dart = 1
        current_turn = request.session['CurrentTurn']
        current_turn += 1
        request.session['CurrentTurn'] = current_turn
        order = ((obj_lnkgameplayer.Order + 1) % request.session['nbPlayer']) if ((obj_lnkgameplayer.Order + 1) % request.session['nbPlayer'] != 0) else request.session['nbPlayer']
        current_player = LnkGamePlayer.objects.get(Game=obj_game, Order=order).Player
    
    request.session['pkCurrentPlayer'] = current_player.pk
    request.session['CurrentDart'] = current_dart

    return request


    