
from darts.models import RefGame

obj = RefGame(GameName = "Cricket - Cut the throat", IsScoreDecreasing = False)
obj.save()
obj = RefGame(GameName = "Cricket - Standard", IsScoreDecreasing = False)
obj.save()
obj = RefGame(GameName = "301", IsScoreDecreasing = True)
obj.save()
obj = RefGame(GameName = "501", IsScoreDecreasing = True)
obj.save()
obj = RefGame(GameName = "701", IsScoreDecreasing = True)
obj.save()