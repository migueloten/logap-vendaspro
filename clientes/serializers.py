from rest_framework import serializers
from .models import Cliente


class ClienteSerializer(serializers.ModelSerializer):
    total_pedidos = serializers.ReadOnlyField()
    valor_total_gasto = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'email', 'contato', 
            'total_pedidos', 'valor_total_gasto',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Validar se o email é único"""
        if self.instance:
            if Cliente.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("Já existe um cliente com este email.")
        else:
            if Cliente.objects.filter(email=value).exists():
                raise serializers.ValidationError("Já existe um cliente com este email.")
        return value


class ClienteListSerializer(serializers.ModelSerializer):
    """Serializer para listagem de clientes"""
    total_pedidos = serializers.ReadOnlyField()
    valor_total_gasto = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'total_pedidos', 'valor_total_gasto']


class ClienteSelectSerializer(serializers.ModelSerializer):
    """Serializer para select de clientes"""
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'email']


class ClienteDetalhesSerializer(serializers.ModelSerializer):
    """Serializer para detalhes do cliente com histórico de pedidos"""
    total_pedidos = serializers.ReadOnlyField()
    valor_total_gasto = serializers.ReadOnlyField()
    
    class Meta:
        model = Cliente
        fields = [
            'id', 'nome', 'email', 'contato', 
            'total_pedidos', 'valor_total_gasto',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
