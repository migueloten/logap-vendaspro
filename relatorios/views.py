from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from clientes.models import Cliente
from produtos.models import Produto
from pedidos.models import Pedido, PedidoItem


class RelatorioViewSet(viewsets.ViewSet):
    """ViewSet para relatórios do sistema"""
    
    @action(detail=False, methods=['get'])
    def vendas_periodo(self, request):
        """Relatório de vendas por período"""
        data_inicio = request.query_params.get('data_inicio')
        data_fim = request.query_params.get('data_fim')
        
        if not data_inicio or not data_fim:
            return Response(
                {'error': 'data_inicio e data_fim são obrigatórios'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {'error': 'Formato de data inválido. Use YYYY-MM-DD'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        pedidos = Pedido.objects.filter(
            data_criacao__date__range=[data_inicio, data_fim],
            status='Finalizado'
        )
        
        relatorio = {
            'periodo': {
                'inicio': data_inicio,
                'fim': data_fim
            },
            'total_vendas': pedidos.count(),
            'valor_total': pedidos.aggregate(Sum('total'))['total__sum'] or 0,
            'valor_medio': pedidos.aggregate(Avg('total'))['total__avg'] or 0,
            'vendas_por_dia': list(
                pedidos.values('data_criacao__date')
                .annotate(
                    total_vendas=Count('id'),
                    valor_total=Sum('total')
                )
                .order_by('data_criacao__date')
            )
        }
        
        return Response(relatorio)
    
    @action(detail=False, methods=['get'])
    def produtos_mais_vendidos(self, request):
        """Relatório dos produtos mais vendidos"""
        limite = int(request.query_params.get('limite', 10))
        
        produtos_vendidos = (
            PedidoItem.objects
            .filter(pedido__status='Finalizado')
            .values('produto__nome', 'produto__codigo')
            .annotate(
                quantidade_vendida=Sum('quantidade'),
                valor_total=Sum('subtotal')
            )
            .order_by('-quantidade_vendida')[:limite]
        )
        
        return Response(list(produtos_vendidos))
    
    @action(detail=False, methods=['get'])
    def clientes_top(self, request):
        """Relatório dos melhores clientes"""
        limite = int(request.query_params.get('limite', 10))
        
        clientes_top = (
            Cliente.objects
            .filter(pedidos__status='Finalizado')
            .annotate(
                total_compras=Sum('pedidos__total'),
                numero_pedidos=Count('pedidos')
            )
            .order_by('-total_compras')[:limite]
        )
        
        data = []
        for cliente in clientes_top:
            data.append({
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email,
                'total_compras': cliente.total_compras,
                'numero_pedidos': cliente.numero_pedidos
            })
        
        return Response(data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Dados para dashboard principal"""
        hoje = timezone.now().date()
        mes_atual = hoje.replace(day=1)
        mes_anterior = (mes_atual - timedelta(days=1)).replace(day=1)
        
        # Estatísticas gerais
        total_clientes = Cliente.objects.filter(ativo=True).count()
        total_produtos = Produto.objects.filter(ativo=True).count()
        pedidos_pendentes = Pedido.objects.filter(
            status__in=['Pendente', 'Processando', 'Em progresso']
        ).count()
        
        # Vendas do mês atual
        vendas_mes_atual = Pedido.objects.filter(
            data_criacao__date__gte=mes_atual,
            status='Finalizado'
        ).aggregate(
            total=Sum('total'),
            quantidade=Count('id')
        )
        
        # Vendas do mês anterior
        vendas_mes_anterior = Pedido.objects.filter(
            data_criacao__date__gte=mes_anterior,
            data_criacao__date__lt=mes_atual,
            status='Finalizado'
        ).aggregate(
            total=Sum('total'),
            quantidade=Count('id')
        )
        
        dashboard_data = {
            'estatisticas_gerais': {
                'total_clientes': total_clientes,
                'total_produtos': total_produtos,
                'pedidos_pendentes': pedidos_pendentes
            },
            'vendas_mes_atual': {
                'valor_total': vendas_mes_atual['total'] or 0,
                'quantidade_pedidos': vendas_mes_atual['quantidade'] or 0
            },
            'vendas_mes_anterior': {
                'valor_total': vendas_mes_anterior['total'] or 0,
                'quantidade_pedidos': vendas_mes_anterior['quantidade'] or 0
            }
        }
        
        return Response(dashboard_data)
