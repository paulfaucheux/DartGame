from django.db import models
# Create your models here.


class Dart(models.Model):
    DartName     = models.CharField(max_length = 100)
    TotalValue   = models.IntegerField()
    TimeValue    = models.IntegerField()
    ValueDart    = models.CharField(max_length = 2)
    
    def __str__(self):
        return str(self.DartName)

    def __unicode__(self): #used fr python2
        return str(self.DartName)
    
class Player(models.Model):
    PlayerName = models.CharField(max_length = 200)
    
    def __str__(self):
        return str(self.PlayerName)

    def __unicode__(self): #used fr python2
        return str(self.PlayerName)
        
class RefGame(models.Model):
    GameName            = models.CharField(max_length=200)
    IsScoreDecreasing   = models.BooleanField()
    
    def __str__(self):
        return str(self.GameName) + ' IsScoreDecreasing ' + str(self.IsScoreDecreasing)

    def __unicode__(self): #used fr python2
        return str(self.GameName) + ' IsScoreDecreasing ' + str(self.IsScoreDecreasing)

class Game(models.Model):
    GameName    = models.ForeignKey(RefGame, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    
    def init(self):
        if(self.GameName.GameName == 'Cricket - Cut the throat') | (self.GameName.GameName == 'Cricket - Standard'):
            all_players_to_init = LnkGamePlayer.objects.filter(Game = self)
            if (all_players_to_init is None):
                raise 'init_cricket: there is no player linked to the game'
            else:
                for game_player in all_players_to_init:
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 8
                       , ScoreName = 'Score'
                       ) 
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 1
                       , ScoreName = '20'
                       ) 
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 2
                       , ScoreName = '19'
                       ) 
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 3
                       , ScoreName = '18'
                       ) 
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 4
                       , ScoreName = '17'
                       )
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 5
                       , ScoreName = '16'
                       ) 
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 6
                       , ScoreName = '15'
                       )
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 0
                       , DisplayOrder = 7
                       , ScoreName = '25'
                       )
        elif(self.GameName.GameName == '301'):
            all_players_to_init = LnkGamePlayer.objects.filter(Game = self)
            if (all_players_to_init is None):
                raise 'init_cricket: there is no player linked to the game'
            else:
                for game_player in all_players_to_init:
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 301
                       , DisplayOrder = 1
                       , ScoreName = 'Score'
                       ) 
        elif(self.GameName.GameName == '501'):
            all_players_to_init = LnkGamePlayer.objects.filter(Game = self)
            if (all_players_to_init is None):
                raise 'init_cricket: there is no player linked to the game'
            else:
                for game_player in all_players_to_init:
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 501
                       , DisplayOrder = 1
                       , ScoreName = 'Score'
                       )
        elif(self.GameName.GameName == '701'):
            all_players_to_init = LnkGamePlayer.objects.filter(Game = self)
            if (all_players_to_init is None):
                raise 'init_cricket: there is no player linked to the game'
            else:
                for game_player in all_players_to_init:
                    LnkGamePlayerScore.objects.create(
                       LnkGamePlayer = game_player
                       , ScoreValue = 701
                       , DisplayOrder = 1
                       , ScoreName = 'Score'
                       )
        else:
            raise "Game init: The Game that you want to start does not exist"

class LnkGamePlayer(models.Model):
    Player      = models.ForeignKey(Player, on_delete=models.CASCADE)
    Game        = models.ForeignKey(Game, on_delete=models.CASCADE)
    Order       = models.IntegerField()

    def __str__(self):
        return str(self.Game.GameName) + str(self.Player.PlayerName)

    def __unicode__(self): #used fr python2
        return str(self.Game.GameName) + str(self.Player.PlayerName)
    
    def save(self, *args, **kwargs):
        if self.Player == None:
            raise "LnkGamePlayer save: There is no player for this Game"
        if self.Game == None:
            raise "LnkGamePlayer save: There is no RefGame for this Game"
        if (self.Order == None):
            self.Order = LnkGamePlayer.objects.filter(Game=self.Game).count() + 1   
        super(LnkGamePlayer, self).save(*args, **kwargs)

    
class LnkGamePlayerDartPlayed(models.Model):
    LnkGamePlayer   = models.ForeignKey(LnkGamePlayer, on_delete=models.CASCADE)
    Dart            = models.ForeignKey(Dart, on_delete=models.CASCADE)    
    Turn            = models.IntegerField()
    TurnDart        = models.IntegerField() ## Use to identify when the player had twice the same dart in the same game
    
    def __str__(self):
        return str(self.Dart)

    def __unicode__(self): #used fr python2
        return str(self.Dart)
        
    def save(self, *args, **kwargs):
        if self.Dart == None:
            raise "LnkGamePlayerDartPlayed save: There is no dart for this ScoreBoard"
        if self.Turn == None:
            raise "LnkGamePlayerDartPlayed save: There is no turn for this ScoreBoard"
        if self.LnkGamePlayer == None:
            raise "LnkGamePlayerDartPlayed save: There is no LnkGamePlayer for this ScoreBoard"
        super(LnkGamePlayerDartPlayed, self).save(*args, **kwargs)
    
class LnkGamePlayerScore(models.Model):
    LnkGamePlayer   = models.ForeignKey(LnkGamePlayer, on_delete=models.CASCADE)
    ScoreValue      = models.IntegerField()
    DisplayOrder    = models.IntegerField()
    ScoreName       = models.CharField(max_length=6)

    
    def __str__(self):
        return str(self.LnkGamePlayer)+ str(self.ScoreName)+ str(self.ScoreValue)

    def __unicode__(self): #used fr python2
        return str(self.LnkGamePlayer)+ str(self.ScoreName)+ str(self.ScoreValue)


class LnkDartPlayedScoreUpdate(models.Model):
    DartPlayed      = models.ForeignKey(LnkGamePlayerDartPlayed, on_delete=models.CASCADE)
    Player          = models.ForeignKey(Player, on_delete=models.CASCADE)
    ScoreName       = models.CharField(max_length=6)
    ScoreValue      = models.IntegerField()

    def __str__(self):
        return str(self.Player.PlayerName) + ' Score Name: ' + str(self.ScoreName) + ' Score Value: ' + str(self.ScoreValue)

    def __unicode__(self): #used fr python2
        return str(self.Player.PlayerName) + str(self.ScoreName) +  str(self.ScoreValue)
