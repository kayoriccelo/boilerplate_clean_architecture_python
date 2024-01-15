from django.urls import path

from src.infrastructure.api.django.account import viewsets


urlpatterns = [
    path('<int:pk>/', viewsets.AccountGetViewSet.as_view()),
    path('list/', viewsets.AccountListViewSet.as_view()),
    path('create/', viewsets.AccountCreateViewSet.as_view()),
    path('update/<int:pk>/', viewsets.AccountUpdateViewSet.as_view()),
    path('delete/<int:pk>/', viewsets.AccountDeleteViewSet.as_view()),
]
