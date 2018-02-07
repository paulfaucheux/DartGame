from django.contrib import admin

from .models import Dart, Player, RefGame, Game, LnkGamePlayer

# Register your models here.


admin.site.register(Dart)
admin.site.register(Player)
admin.site.register(RefGame)
admin.site.register(Game)
admin.site.register(LnkGamePlayer)


