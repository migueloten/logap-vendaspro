from rest_framework import serializers
from django.db import transaction
from .models import Pedido, PedidoItem
from clientes.serializers import ClienteSelectSerializer
from produtos.serializers import ProdutoSelectSerializer


class PedidoItemSerializer(serializers.ModelSerializer):
    produto_nome = serializers.CharField(source='produto.nome', read_only=True)
    produto_preco = serializers.DecimalField(source='produto.preco', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = PedidoItem
        fields = [
            'id', 'produto', 'produto_nome', 'produto_preco',
            'quantidade', 'preco_unitario', 'valor_total'
        ]
        read_only_fields = ['id', 'valor_total']

    def validate_quantidade(self, value):
        if value <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return value

    def validate_preco_unitario(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço unitário deve ser maior que zero.")
        return value


class PedidoListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de pedidos"""
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    data_pedido_formatada = serializers.DateTimeField(source='data_pedido', format='%d/%m/%Y', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'cliente_nome', 'status', 
            'total', 'data_pedido', 'data_pedido_formatada'
        ]


class PedidoDetalhesSerializer(serializers.ModelSerializer):
    """Serializer para detalhes do pedido"""
    cliente = ClienteSelectSerializer(read_only=True)
    itens = PedidoItemSerializer(many=True, read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    total_produtos_vendidos = serializers.ReadOnlyField()
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'cliente', 'status', 'subtotal', 'frete', 'total',
            'endereco_cep', 'endereco_cidade', 'endereco_uf', 'endereco_rua',
            'endereco_numero', 'endereco_complemento', 'endereco_completo',
            'metodo_envio', 'data_pedido', 'itens', 'total_produtos_vendidos'
        ]


class PedidoCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de pedidos"""
    itens = PedidoItemSerializer(many=True, write_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'frete', 'metodo_envio',
            'endereco_cep', 'endereco_cidade', 'endereco_uf', 
            'endereco_rua', 'endereco_numero', 'endereco_complemento',
            'itens'
        ]

    def validate_itens(self, value):
        if not value:
            raise serializers.ValidationError("O pedido deve ter pelo menos um item.")
        return value

    def validate_frete(self, value):
        if value < 0:
            raise serializers.ValidationError("O frete não pode ser negativo.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        
        # Calcular subtotal com base nos itens
        from decimal import Decimal
        subtotal = Decimal('0.00')
        for item_data in itens_data:
            preco_unitario = item_data.get('preco_unitario', item_data['produto'].preco)
            quantidade = item_data['quantidade']
            subtotal += Decimal(str(preco_unitario)) * quantidade
        
        # Definir valores calculados
        validated_data['subtotal'] = subtotal
        frete = Decimal(str(validated_data.get('frete', 0)))
        validated_data['total'] = subtotal + frete
        
        # Criar o pedido com total calculado
        pedido = Pedido.objects.create(**validated_data)
        
        # Criar os itens
        for item_data in itens_data:
            # Se o preço unitário não foi fornecido, usar o preço do produto
            if 'preco_unitario' not in item_data:
                item_data['preco_unitario'] = item_data['produto'].preco
            
            PedidoItem.objects.create(pedido=pedido, **item_data)
        return pedido


class PedidoUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de pedidos"""
    itens = PedidoItemSerializer(many=True, required=False)
    
    class Meta:
        model = Pedido
        fields = [
            'cliente', 'frete', 'metodo_envio',
            'endereco_cep', 'endereco_cidade', 'endereco_uf', 
            'endereco_rua', 'endereco_numero', 'endereco_complemento',
            'itens'
        ]

    def validate_frete(self, value):
        if value < 0:
            raise serializers.ValidationError("O frete não pode ser negativo.")
        return value

    @transaction.atomic
    def update(self, instance, validated_data):
        itens_data = validated_data.pop('itens', None)
        
        # Atualizar dados do pedido
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Se itens foram fornecidos, atualizar
        if itens_data is not None:
            # Remover itens existentes
            instance.itens.all().delete()
            
            # Criar novos itens
            for item_data in itens_data:
                if 'preco_unitario' not in item_data:
                    item_data['preco_unitario'] = item_data['produto'].preco
                
                PedidoItem.objects.create(pedido=instance, **item_data)
        
        # Recalcular total
        instance.calcular_total()
        return instance


class PedidoPendenteSerializer(serializers.ModelSerializer):
    """Serializer para pedidos pendentes"""
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    data_pedido_formatada = serializers.DateTimeField(source='data_pedido', format='%d/%m/%Y', read_only=True)
    
    class Meta:
        model = Pedido
        fields = [
            'id', 'numero', 'cliente_nome', 'data_pedido_formatada', 
            'status', 'total'
        ]


class PedidoHistoricoClienteSerializer(serializers.ModelSerializer):
    """Serializer para histórico de pedidos do cliente"""
    
    class Meta:
        model = Pedido
        fields = ['id', 'numero', 'data_pedido', 'status', 'total']
        read_only_fields = ['id', 'numero', 'data_pedido', 'status', 'total']


class PedidoSerializer(serializers.ModelSerializer):
    """Serializer principal para pedidos"""
    cliente_nome = serializers.CharField(source='cliente.nome', read_only=True)
    
    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ['id', 'numero', 'total', 'created_at', 'updated_at']
