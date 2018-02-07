import pandas as pd

from django.core import serializers

from darts.models import Game, Player, LnkGamePlayer, LnkGamePlayerScore, LnkGamePlayerDartPlayed, Dart, LnkDartPlayedScoreUpdate



def getScoreArray(obj_game):
    df_score = pd.DataFrame()
    
    for obj_LnkGamePlayer in LnkGamePlayer.objects.filter(Game=obj_game):
        str_player = obj_LnkGamePlayer.Player.PlayerName
        
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

def addLnkDartPlayedScoreUpdate(dartPlayed,player,scoreName,scoreValue):
    print('The player {} played {} for a value of {}'.format(player.PlayerName, dartPlayed.Dart.DartName, scoreValue))
    LnkDartPlayedScoreUpdate.objects.create(DartPlayed = dartPlayed,Player = player,ScoreName = scoreName,ScoreValue = scoreValue)
    return None

def updateScoreOtherPlayersCricket(dart, extra_score, obj_game, obj_DartPlayed,current_turn):
    players_score = LnkGamePlayerScore.objects.filter(LnkGamePlayer__in= LnkGamePlayer.objects.filter(Game=obj_game), ScoreName = dart.ValueDart)
    for player in players_score:
        if player.ScoreValue < 3:
            main_player_score = LnkGamePlayerScore.objects.get(LnkGamePlayer = player.LnkGamePlayer, ScoreName='Score')
            main_player_score.ScoreValue += int(dart.ValueDart) * extra_score
            main_player_score.save()
            addLnkDartPlayedScoreUpdate(obj_DartPlayed, player.LnkGamePlayer.Player ,'Score',int(dart.ValueDart) * extra_score)

def updateScoreCurrentPlayerCricket(lnkGamePlayer, score, dart, obj_DartPlayed,current_turn):
    main_player_score = LnkGamePlayerScore.objects.get(LnkGamePlayer = lnkGamePlayer, ScoreName='Score')
    main_player_score.ScoreValue += score
    main_player_score.save()
    addLnkDartPlayedScoreUpdate(obj_DartPlayed,obj_DartPlayed.LnkGamePlayer.Player,'Score',score)
     


def updateScoreCurrentPlayer(obj_DartPlayed, request):

    obj_game = Game.objects.get(pk=obj_DartPlayed.LnkGamePlayer.Game.pk)
    dart = Dart.objects.get(pk=obj_DartPlayed.Dart.pk)
    current_scores = LnkGamePlayerScore.objects.filter(LnkGamePlayer=obj_DartPlayed.LnkGamePlayer)
    current_turn = request.session['CurrentTurn']
    
    if obj_game.GameName.GameName == 'Cricket - Cut the throat':
        for score in current_scores:
            if score.ScoreName == dart.ValueDart:
                score.ScoreValue += dart.TimeValue
                score.save()
                if score.ScoreValue > 3:
                    extra_score = score.ScoreValue - 3
                    score.ScoreValue = 3
                    score.save()
                    updateScoreOtherPlayersCricket(dart, extra_score, obj_game, obj_DartPlayed,current_turn)
                else:
                    addLnkDartPlayedScoreUpdate(obj_DartPlayed,obj_DartPlayed.LnkGamePlayer.Player,dart.ValueDart,dart.TimeValue)
    elif obj_game.GameName.GameName == 'Cricket - Standard':
        for score in current_scores:
            if score.ScoreName == dart.ValueDart:
                score.ScoreValue += dart.TimeValue
                score.save()
                if score.ScoreValue > 3:
                    extra_score = score.ScoreValue - 3
                    score.ScoreValue = 3
                    score.save()
                    updateScoreCurrentPlayerCricket(obj_DartPlayed.LnkGamePlayer, int(dart.ValueDart) * extra_score, dart, obj_DartPlayed,current_turn)
                else:
                    addLnkDartPlayedScoreUpdate(obj_DartPlayed,obj_DartPlayed.LnkGamePlayer.Player,dart.ValueDart,dart.TimeValue)
    elif obj_game.GameName.GameName in ['301','501','701']:
        for score in current_scores:
            if score.ScoreName == 'Score':
                if dart.TotalValue <= score.ScoreValue:
                    score.ScoreValue -= dart.TotalValue
                    score.save()
                    addLnkDartPlayedScoreUpdate(obj_DartPlayed,obj_DartPlayed.LnkGamePlayer.Player,'Score',dart.TotalValue)               
    else:
        raise 'No rules to update the score for game {0}'.format(obj_game.GameName.GameName)
    
        
    

def newDartPlayed(the_form_dart, request):
    

    
    obj_game = Game.objects.get(pk=int(request.session['pkGame']))
    current_player = Player.objects.get(pk=int(request.session['pkCurrentPlayer']))
    current_dart = request.session['CurrentDart']
    current_turn = request.session['CurrentTurn']
    
    
    obj_lnkgameplayer = LnkGamePlayer.objects.get(Game=obj_game, Player=current_player)

    obj_DartPlayed = LnkGamePlayerDartPlayed.objects.create(
        LnkGamePlayer=obj_lnkgameplayer
        , Dart = Dart.objects.get(DartName=str(the_form_dart.cleaned_data['dart1']))
        , Turn = current_turn
        , TurnDart = current_dart
    )
    
    updateScoreCurrentPlayer(obj_DartPlayed, request)
    
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

def cancelLastDart(request):
    current_dart = request.session['CurrentDart']
    current_dart -= 1
    if current_dart <= 0:
        current_dart = 1
        current_turn = request.session['CurrentTurn']
        current_turn -= 1
        request.session['CurrentTurn'] = current_turn
    request.session['CurrentDart'] = current_dart
    
    last_dart_played = LnkGamePlayerDartPlayed.objects.last()
    #print('last_played dart: {}'.format(last_dart_played))
    for score_to_update in LnkDartPlayedScoreUpdate.objects.filter(DartPlayed=last_dart_played):
        #print('Score: {}'.format(score_to_update))
      
        new_LnkGamePlayer = LnkGamePlayer.objects.get(
            Game = score_to_update.DartPlayed.LnkGamePlayer.Game
            , Player = score_to_update.Player)
        new_score = LnkGamePlayerScore.objects.get(
            LnkGamePlayer = new_LnkGamePlayer
            , ScoreName = score_to_update.ScoreName) 
        #print('old_score: {}\tnew_score: {}'.format(new_score.ScoreValue, score_to_update.ScoreValue ))
        if score_to_update.DartPlayed.LnkGamePlayer.Game.GameName.IsScoreDecreasing:
            new_score.ScoreValue = new_score.ScoreValue + score_to_update.ScoreValue
        else:
            new_score.ScoreValue = new_score.ScoreValue - score_to_update.ScoreValue
        new_score.save()
        
    return None
    