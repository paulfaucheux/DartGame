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


class LnkGamePlayer(models.Model):
    Player          = models.ForeignKey(Player, on_delete=models.CASCADE)
    Dart            = models.ForeignKey(Dart, on_delete=models.CASCADE)
    RefGame         = models.ForeignKey(RefGame, on_delete=models.CASCADE)
    Turn            = models.IntegerField()
    ScoreValue      = models.IntegerField()
    
    def __str__(self):
        return str(self.Turn)

    def __unicode__(self): #used fr python2
        return str
    
    def save(self, *args, **kwargs):
        
        if self.Player == None:
            raise "DartPlayed save: There is no player for this ScoreBoard"
        if self.Game == None:
            raise "DartPlayed save: There is no game for this ScoreBoard"
        if self.Dart == None:
            raise "DartPlayed save: There is no dart for this ScoreBoard"
        super(LnkGamePlayer, self).save(*args, **kwargs)

    
