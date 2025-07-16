from django.urls import path
from . import views

urlpatterns = [
    path('processar/', views.encontrar_vogal_especial, name='processar_vogal'),
    path('exemplo/', views.exemplo_uso, name='exemplo_uso'),
]
