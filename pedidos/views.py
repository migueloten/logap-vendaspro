from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Pedido, PedidoItem
from .serializers import (
    PedidoSerializer, PedidoListSerializer, PedidoCreateSerializer,
    PedidoDetalhesSerializer, PedidoHistoricoClienteSerializer
)


@method_decorator(csrf_exempt, name='dispatch')
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.select_related('cliente').prefetch_related('itens__produto').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'cliente']
    search_fields = ['numero', 'cliente__nome']
    ordering_fields = ['data_pedido', 'total', 'numero']
    ordering = ['-data_pedido']

    def get_serializer_class(self):
        if self.action == 'create':
            return PedidoCreateSerializer
        elif self.action == 'list':
            return PedidoListSerializer
        elif self.action == 'detalhes':
            return PedidoDetalhesSerializer
        return PedidoSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtro por nome do cliente
        nome_cliente = self.request.query_params.get('nome_cliente')
        if nome_cliente:
            queryset = queryset.filter(cliente__nome__icontains=nome_cliente)
        
        # Filtro por número do pedido
        numero = self.request.query_params.get('numero')
        if numero:
            queryset = queryset.filter(numero__icontains=numero)
        
        # Filtro por status
        status_filtro = self.request.query_params.get('status')
        if status_filtro:
            queryset = queryset.filter(status=status_filtro)
        
        return queryset

    @action(detail=True, methods=['get'])
    def detalhes(self, request, pk=None):
        """Detalhes completos do pedido"""
        pedido = self.get_object()
        serializer = PedidoDetalhesSerializer(pedido)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def alterar_status(self, request, pk=None):
        """Altera o status de um pedido"""
        pedido = self.get_object()
        novo_status = request.data.get('status')
        
        if not novo_status:
            return Response(
                {'error': 'Status é obrigatório'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if novo_status not in [choice[0] for choice in Pedido.STATUS_CHOICES]:
            return Response(
                {'error': 'Status inválido'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Atualizar status
        pedido.status = novo_status
        pedido.save()
        
        return Response({
            'message': 'Status atualizado com sucesso',
            'pedido': PedidoSerializer(pedido).data
        })

    @action(detail=False, methods=['get'])
    def pendentes(self, request):
        """Pedidos pendentes"""
        pedidos = self.get_queryset().filter(status='pendente')
        serializer = PedidoListSerializer(pedidos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_status(self, request):
        """Agrupamento de pedidos por status"""
        dados = {}
        for status_choice in Pedido.STATUS_CHOICES:
            status_key = status_choice[0]
            status_label = status_choice[1]
            count = self.get_queryset().filter(status=status_key).count()
            dados[status_key] = {
                'label': status_label,
                'count': count
            }
        return Response(dados)

    @action(detail=False, methods=['get'])
    def historico_vendas(self, request):
        """Histórico de vendas (para dashboard)"""
        from django.db.models import Sum, Count
        from datetime import datetime, timedelta
        
        # Dados dos últimos 30 dias
        data_inicio = datetime.now().date() - timedelta(days=30)
        
        vendas = self.get_queryset().filter(
            data_pedido__gte=data_inicio
        ).values('data_pedido').annotate(
            total_vendas=Sum('total'),
            quantidade_pedidos=Count('id')
        ).order_by('data_pedido')
        


class PedidoItemViewSet(viewsets.ModelViewSet):
    queryset = PedidoItem.objects.select_related('pedido', 'produto').all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['pedido', 'produto']
    
    def get_serializer_class(self):
        from .serializers import PedidoItemSerializer
        return PedidoItemSerializer
