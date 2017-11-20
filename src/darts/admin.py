from django.contrib import admin

from darts.models import Dart, Player, RefGame, Game, DartPlayed, PlayerScore

# Register your models here.


admin.site.register(Dart)
admin.site.register(RefGame)
admin.site.register(Player)
admin.site.register(Game)
admin.site.register(DartPlayed)
admin.site.register(PlayerScore)

