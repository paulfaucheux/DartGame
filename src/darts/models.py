from django.db import models
# Create your models here.


class Dart(models.Model):
    DartName    = models.CharField(max_length = 100)
    DartValue   = models.IntegerField()
    
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
    GameName = models.CharField(max_length=200)
    
    def __str__(self):
        return str(self.GameName)

    def __unicode__(self): #used fr python2
        return str(self.GameName)

class Game(models.Model):
    GameName    = models.ForeignKey(RefGame, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    
    def init(self):
        if(self.GameName.GameName == 'Cricket'):
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
                       , ScoreName = 'B'
                       )
        else:
            raise "Game init: The Game that you want to start does not exist"

class LnkGamePlayer(models.Model):
    Player      = models.ForeignKey(Player, on_delete=models.CASCADE)
    Game        = models.ForeignKey(Game, on_delete=models.CASCADE)
    Order       = models.IntegerField()

    def __str__(self):
        return [str(self.Game), str(self.Player)]

    def __unicode__(self): #used fr python2
        return [str(self.Game), str(self.Player)]
    
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
        return str(self.LnkGamePlayer), str(self.ScoreName), str(self.ScoreValue)

    def __unicode__(self): #used fr python2
        return str(self.LnkGamePlayer), str(self.ScoreName), str(self.ScoreValue)
    