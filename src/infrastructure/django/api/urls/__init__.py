from django.urls import include, path


urlpatterns = [
    path("accounts/", include("src.infrastructure.django.api.urls.account")),
    path("brokers/", include("src.infrastructure.django.api.urls.broker")),
    path("active/", include("src.infrastructure.django.api.urls.active")),
]
