from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_metrics, name='dashboard-metrics'),
    path('relatorios/pedidos-pendentes/', views.relatorio_pedidos_pendentes, name='relatorio-pedidos-pendentes'),
    path('relatorios/clientes-ativos/', views.relatorio_clientes_ativos, name='relatorio-clientes-ativos'),
    path('relatorios/geral/', views.relatorio_geral, name='relatorio-geral'),
]
