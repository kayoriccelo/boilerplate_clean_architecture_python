from django.contrib import admin

from .models import ManagementModel, ManagementByStrategyModel


admin.site.register(ManagementModel)
admin.site.register(ManagementByStrategyModel)
