from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente
from .serializers import (
    ClienteSerializer, ClienteListSerializer, 
    ClienteSelectSerializer, ClienteDetalhesSerializer
)
from pedidos.serializers import PedidoHistoricoClienteSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nome', 'email']
    ordering_fields = ['nome', 'created_at']
    ordering = ['nome']

    def get_serializer_class(self):
        if self.action == 'list':
            return ClienteListSerializer
        elif self.action == 'select':
            return ClienteSelectSerializer
        elif self.action == 'detalhes':
            return ClienteDetalhesSerializer
        return ClienteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por nome
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        
        return queryset

    @action(detail=False, methods=['get'])
    def select(self, request):
        """Endpoint para select de clientes"""
        clientes = self.get_queryset()
        serializer = ClienteSelectSerializer(clientes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def detalhes(self, request, pk=None):
        """Detalhes do cliente com histórico de pedidos"""
        cliente = self.get_object()
        
        # Dados do cliente
        cliente_serializer = ClienteDetalhesSerializer(cliente)
        
        # Histórico de pedidos
        pedidos = cliente.pedidos.all().order_by('-data_pedido')
        pedidos_serializer = PedidoHistoricoClienteSerializer(pedidos, many=True)
        
        return Response({
            'cliente': cliente_serializer.data,
            'historico_pedidos': pedidos_serializer.data
        })

    @action(detail=False, methods=['get'])
    def mais_ativos(self, request):
        """Clientes mais ativos (para relatórios)"""
        limite = int(request.query_params.get('limite', 10))
        
        # Buscar clientes ordenados por valor total gasto
        clientes = self.get_queryset().order_by('-total_pedidos')[:limite]
        
        dados = []
        for cliente in clientes:
            dados.append({
                'cliente': cliente.nome,
                'total_pedidos': cliente.total_pedidos,
                'total_gasto': cliente.valor_total_gasto
            })
        
        return Response(dados)
