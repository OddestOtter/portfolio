from rest_framework.routers import DefaultRouter
from django.urls import apirouter
from .views import CoreModelViewSet

router = DefaultRouter()
router.register(r'core', CoreModelViewSet)

urlpatterns = router.urls
