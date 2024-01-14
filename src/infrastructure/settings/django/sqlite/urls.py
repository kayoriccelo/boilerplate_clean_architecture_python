from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-auth/', include('rest_framework.urls')),

    path("api/v1/accounts/", include("src.infrastructure.api.django.account.urls")),
]
