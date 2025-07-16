from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from pedidos.models import Pedido
from clientes.models import Cliente
from produtos.models import Produto


@api_view(['GET'])
def dashboard_metrics(request):
    """Métricas do dashboard"""
    today = datetime.now().date()
    
    # Total de pedidos
    total_pedidos = Pedido.objects.count()
    
    # Faturamento total
    faturamento_total = Pedido.objects.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Produtos vendidos (quantidade total de itens)
    produtos_vendidos = Pedido.objects.aggregate(
        total=Sum('itens__quantidade')
    )['total'] or 0
    
    # Histórico de vendas dos últimos 30 dias
    data_inicio = today - timedelta(days=30)
    historico_vendas = Pedido.objects.filter(
        data_pedido__gte=data_inicio
    ).values('data_pedido').annotate(
        vendas=Sum('total')
    ).order_by('data_pedido')
    
    # Formatar dados do histórico
    historico_formatado = []
    for item in historico_vendas:
        historico_formatado.append({
            'data': item['data_pedido'].strftime('%Y-%m-%d'),
            'vendas': float(item['vendas'])
        })
    
    return Response({
        'total_pedidos': total_pedidos,
        'faturamento_total': float(faturamento_total),
        'produtos_vendidos': produtos_vendidos,
        'historico_vendas': historico_formatado
    })


@api_view(['GET'])
def relatorio_pedidos_pendentes(request):
    """Relatório de pedidos pendentes"""
    pedidos = Pedido.objects.filter(status=Pedido.StatusChoices.PENDENTE).select_related('cliente')
    
    dados = []
    for pedido in pedidos:
        dados.append({
            'numero': pedido.numero,
            'cliente': pedido.cliente.nome,
            'total': float(pedido.total),
            'data_pedido': pedido.data_pedido.strftime('%Y-%m-%d'),
            'endereco': f"{pedido.endereco_rua}, {pedido.endereco_numero} - {pedido.endereco_cidade}/{pedido.endereco_uf}"
        })
    
    return Response(dados)


@api_view(['GET'])
def relatorio_clientes_ativos(request):
    """Relatório de clientes mais ativos"""
    limite = int(request.query_params.get('limite', 10))
    
    clientes = Cliente.objects.annotate(
        total_pedidos_count=Count('pedidos')
    ).order_by('-total_pedidos_count')[:limite]
    
    dados = []
    for cliente in clientes:
        dados.append({
            'cliente': cliente.nome,
            'total_pedidos': cliente.total_pedidos,
            'valor_total': float(cliente.valor_total_gasto)
        })
    
    return Response(dados)


@api_view(['GET'])
def relatorio_geral(request):
    """Relatório geral com estatísticas"""
    # Contadores básicos
    total_clientes = Cliente.objects.count()
    total_produtos = Produto.objects.count()
    total_pedidos = Pedido.objects.count()
    
    # Faturamento total
    faturamento_total = Pedido.objects.aggregate(
        total=Sum('total')
    )['total'] or 0
    
    # Pedidos por status
    pedidos_por_status = {}
    for status_choice in Pedido.StatusChoices.choices:
        status_key = status_choice[0]
        status_label = status_choice[1]
        count = Pedido.objects.filter(status=status_key).count()
        pedidos_por_status[status_key] = {
            'label': status_label,
            'count': count
        }
    
    # Top 5 clientes
    top_clientes = Cliente.objects.annotate(
        total_pedidos_count=Count('pedidos')
    ).order_by('-total_pedidos_count')[:5]
    clientes_dados = []
    for cliente in top_clientes:
        clientes_dados.append({
            'nome': cliente.nome,
            'total_pedidos': cliente.total_pedidos,
            'valor_total': float(cliente.valor_total_gasto)
        })
    
    return Response({
        'totais': {
            'clientes': total_clientes,
            'produtos': total_produtos,
            'pedidos': total_pedidos,
            'faturamento': float(faturamento_total)
        },
        'pedidos_por_status': pedidos_por_status,
        'top_clientes': clientes_dados
    })
