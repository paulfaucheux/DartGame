import pandas as pd

from darts.models import LnkGamePlayer, LnkGamePlayerScore



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

            

