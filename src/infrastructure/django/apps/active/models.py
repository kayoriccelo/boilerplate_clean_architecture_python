from django.db import models

from src.infrastructure.django.apps.active.choices import C_STATUS_ACTIVE, STATUS_ACTIVE_ACTIVE


class ActiveModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    status = models.IntegerField(choices=C_STATUS_ACTIVE, default=STATUS_ACTIVE_ACTIVE)

    account = models.ForeignKey('account.AccountModel', related_name='active', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Active'
        verbose_name_plural = u'Active'
        db_table = 'active'

    def __str__(self) -> str:
        return self.description
