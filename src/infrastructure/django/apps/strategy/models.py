from django.db import models

from src.infrastructure.django.apps.strategy.choices import (
    C_STATUS_STRATEGY, STATUS_STRATEGY_ACTIVE,
    
    C_STATUS_STRATEGY_QUADRANT, STATUS_STRATEGY_QUADRANT_ACTIVE,
    
    C_COLOR_STRATEGY_CANDLE, 
    C_STATUS_STRATEGY_CANDLE, STATUS_STRATEGY_CANDLE_ACTIVE,
    
    C_TYPE_STRATEGY_TIME, 
    C_STATUS_STRATEGY_TIME, STATUS_STRATEGY_TIME_ACTIVE
)


class StrategyModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    status = models.IntegerField(choices=C_STATUS_STRATEGY, default=STATUS_STRATEGY_ACTIVE)
    
    account = models.ForeignKey('account.AccountModel', related_name='strategies', on_delete=models.CASCADE)
    cycles = models.ManyToManyField('cycle.CycleModel', related_name='strategies', blank=True)
    
    class Meta:
        verbose_name = u'Strategy'
        verbose_name_plural = u'Strategies'
        db_table = 'strategy'

    def __str__(self) -> str:
        return self.description


class StrategyQuadrantModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=C_STATUS_STRATEGY_QUADRANT, default=STATUS_STRATEGY_QUADRANT_ACTIVE)

    strategy = models.ForeignKey('strategy.StrategyModel', related_name='strategies_quadrants', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Strategy Quadrant'
        verbose_name_plural = u'Strategies Quadrants'
        db_table = 'strategy_quadrant'


class StrategyTimeModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    type = models.IntegerField(choices=C_TYPE_STRATEGY_TIME)
    status = models.IntegerField(choices=C_STATUS_STRATEGY_TIME, default=STATUS_STRATEGY_TIME_ACTIVE)
   
    strategy_quadrant = models.ForeignKey('strategy.StrategyQuadrantModel', related_name='strategies_times', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Strategy Time'
        verbose_name_plural = u'Strategies Times'
        db_table = 'strategy_time'


class StrategyCandleModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sequence = models.IntegerField(default=0)
    color = models.IntegerField(choices=C_COLOR_STRATEGY_CANDLE)
    compare = models.BooleanField(default=False)
    conditional = models.BooleanField(default=False)
    status = models.IntegerField(choices=C_STATUS_STRATEGY_CANDLE, default=STATUS_STRATEGY_CANDLE_ACTIVE)

    strategy = models.ForeignKey('strategy.StrategyModel', related_name='strategies_candles', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Strategy Candle'
        verbose_name_plural = u'Strategies Candles'
        db_table = 'strategy_candle'

    def __str__(self) -> str:
        return f'{self.sequence} - {self.get_color_display()} - Compare: {self.compare} - Conditional: {self.conditional}'
