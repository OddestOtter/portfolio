from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include API endpoints here
    path('api/v1/', include('apps.core.urls')),
]
