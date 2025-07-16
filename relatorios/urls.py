from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelatorioViewSet

router = DefaultRouter()
router.register(r'relatorios', RelatorioViewSet, basename='relatorios')

urlpatterns = [
    path('', include(router.urls)),
]
