from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
urlpatterns = router.urls
