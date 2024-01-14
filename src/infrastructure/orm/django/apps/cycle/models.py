from django.db import models

from src.infrastructure.orm.django.apps.cycle.choices import C_STATUS_CYCLE, STATUS_CYCLE_ACTIVE


class CycleModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    sequence = models.IntegerField()
    martingale = models.BooleanField(default=False)
    martingale_levels: models.IntegerField(default=0)
    martingale_multipler = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    martingale_reverse = models.BooleanField(default=False)
    serums = models.BooleanField(default=False)
    serums_levels: models.IntegerField(default=0)
    serums_percentage_profit = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.IntegerField(choices=C_STATUS_CYCLE, default=STATUS_CYCLE_ACTIVE)

    account = models.ForeignKey('account.AccountModel', related_name='cycles', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = u'Cycle'
        verbose_name_plural = u'Cycle'
        db_table = 'cycle'

    def __str__(self) -> str:
        return self.sequence
