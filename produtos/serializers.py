from rest_framework import serializers
from .models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco', 'ativo', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_preco(self, value):
        """Validar se o preço é maior que zero"""
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value


class ProdutoSelectSerializer(serializers.ModelSerializer):
    """Serializer para select de produtos"""
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'preco']
