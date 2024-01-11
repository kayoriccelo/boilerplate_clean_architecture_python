from django.urls import path

from src.infrastructure.django.api.views import account


urlpatterns = [
    path('<int:pk>/', account.AccountGetViewSet.as_view()),
    path('list/', account.AccountListViewSet.as_view()),
    path('create/', account.AccountCreateViewSet.as_view()),
    path('update/<int:pk>/', account.AccountUpdateViewSet.as_view()),
    path('delete/<int:pk>/', account.AccountDeleteViewSet.as_view()),
]
