from rest_framework import serializers


class DesafioVogalInputSerializer(serializers.Serializer):
    string = serializers.CharField(
        help_text="String para processar e encontrar a vogal especial",
        required=True,
        allow_blank=False,
        max_length=10000,
        style={'base_template': 'textarea.html'}
    )
    
    def validate_string(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Campo deve ser uma string")
        return value


class DesafioVogalOutputSerializer(serializers.Serializer):
    string = serializers.CharField(
        help_text="String original processada"
    )
    vogal = serializers.CharField(
        help_text="Vogal encontrada ou null se não encontrada",
        allow_null=True
    )
    tempoTotal = serializers.CharField(
        help_text="Tempo total de processamento em milissegundos"
    )


class ExemploUsoSerializer(serializers.Serializer):
    exemplo = serializers.DictField(
        help_text="Exemplo de como usar a API"
    )
    regras = serializers.ListField(
        child=serializers.CharField(),
        help_text="Regras do desafio"
    )
