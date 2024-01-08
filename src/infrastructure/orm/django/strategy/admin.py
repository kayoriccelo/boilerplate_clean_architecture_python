from django.contrib import admin

from .models import StrategyModel, StrategyQuadrantModel, StrategyCandleModel, StrategyTimeModel


admin.site.register(StrategyModel)
admin.site.register(StrategyQuadrantModel)
admin.site.register(StrategyCandleModel)
admin.site.register(StrategyTimeModel)
