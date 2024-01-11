from django.db import models

from src.infrastructure.django.apps.management.choices import C_STATUS_MANAGEMENT, STATUS_MANAGEMENT_ACTIVE


class ManagementModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    payout = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    value_investing = models.DecimalField(max_digits=19, decimal_places=2)
    stop_loss: models.DecimalField(max_digits=19, decimal_places=2)
    stop_win: models.DecimalField(max_digits=19, decimal_places=2)
    time_candle: models.IntegerField()
    number_candles: models.IntegerField()
    expiration: models.IntegerField()
    status = models.IntegerField(choices=C_STATUS_MANAGEMENT, default=STATUS_MANAGEMENT_ACTIVE)
    
    account = models.ForeignKey('account.AccountModel', related_name='managements', on_delete=models.CASCADE)
    active = models.ManyToManyField('active.ActiveModel', related_name='managements')
    cycles = models.ManyToManyField('cycle.CycleModel', related_name='managements', blank=True)

    class Meta:
        verbose_name = u'Management'
        verbose_name_plural = u'Management'
        db_table = 'management'

    def __str__(self) -> str:
        return self.description


class ManagementByStrategyModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    use_candle_color_filter = models.BooleanField(default=False)
    initial_candle_color_filter = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_candle_color_filter = models.DecimalField(max_digits=5, decimal_places=2, default=0) 
    use_candle_color_filter_result = models.BooleanField(default=False)
    initial_candle_color_filter_result = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_candle_color_filter_result = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    use_candle_similarity_filter = models.BooleanField(default=False)
    levels_candle_similarity_filter = models.IntegerField(default=0)
    initial_candle_similarity_filter = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_candle_similarity_filter = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    use_candle_similarity_filter_result = models.BooleanField(default=False)
    levels_candle_similarity_filter_result = models.IntegerField(default=0)
    initial_candle_similarity_filter_result = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_candle_similarity_filter_result = models.DecimalField(max_digits=5, decimal_places=2, default=0) 
    use_trader_mood = models.BooleanField(default=False)
    initial_trader_mood = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    final_trader_mood = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    strategy = models.ForeignKey('strategy.StrategyModel', related_name='managements_by_strategies', on_delete=models.CASCADE)
    management = models.ForeignKey('management.ManagementModel', related_name='managements_by_strategies', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Management By Strategy'
        verbose_name_plural = u'Managements By Strategies'
        db_table = 'management_by_strategy'
  