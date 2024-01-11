from django.db import models

from src.infrastructure.django.apps.broker.choices import C_STATUS_BROKER, STATUS_BROKER_ACTIVE


class BrokerModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    status = models.IntegerField(choices=C_STATUS_BROKER, default=STATUS_BROKER_ACTIVE)
    
    account = models.ForeignKey('account.AccountModel', related_name='brokers', on_delete=models.CASCADE)
    active = models.ManyToManyField('active.ActiveModel', related_name='brokers', blank=True)
    
    class Meta:
        verbose_name = u'Broker'
        verbose_name_plural = u'Broker'
        db_table = 'broker'

    def __str__(self) -> str:
        return self.description
