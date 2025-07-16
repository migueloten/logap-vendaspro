from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PedidoViewSet, PedidoItemViewSet

router = DefaultRouter()
router.register(r'pedidos', PedidoViewSet)
router.register(r'pedido-itens', PedidoItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
