from django.db import models

from src.infrastructure.django.apps.account.choices import C_GENDER_ACCOUNT, C_STATUS_ACCOUNT, STATUS_ACCOUNT_ACTIVE


class AccountModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    number_identity = models.CharField(max_length=100)
    date_birth = models.DateField()
    gender = models.IntegerField(choices=C_GENDER_ACCOUNT)
    status = models.IntegerField(choices=C_STATUS_ACCOUNT, default=STATUS_ACCOUNT_ACTIVE)

    class Meta:
        verbose_name = u'Account'
        verbose_name_plural = u'Accounts'
        db_table = 'account'

    def __str__(self) -> str:
        return f'{self.number_identity} - {self.first_name} - {self.last_name}'
