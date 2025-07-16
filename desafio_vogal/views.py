from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import DesafioVogalInputSerializer, DesafioVogalOutputSerializer, ExemploUsoSerializer
import time


@extend_schema(
    request=DesafioVogalInputSerializer,
    responses=DesafioVogalOutputSerializer,
    summary="Processar String - Desafio Vogal",
    description="Encontra o primeiro caractere vogal após uma consoante, onde a consoante é antecessora a uma vogal e que não se repita na string.",
    examples=[
        OpenApiExample(
            'Exemplo Básico',
            description='Exemplo com a string do desafio',
            value={
                'string': 'aAbBABacafe'
            },
            request_only=True,
        ),
        OpenApiExample(
            'Resposta Esperada',
            description='Resposta com a vogal encontrada',
            value={
                'string': 'aAbBABacafe',
                'vogal': 'e',
                'tempoTotal': '0.16ms'
            },
            response_only=True,
        ),
    ]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def encontrar_vogal_especial(request):

    inicio = time.time()
    
    # Validar entrada usando serializer
    serializer = DesafioVogalInputSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {'erro': serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    input_string = serializer.validated_data['string']
    
    # Encontrar a vogal especial
    vogal_encontrada = processar_string(input_string)
    
    # Calcular tempo total
    fim = time.time()
    tempo_total = round((fim - inicio) * 1000, 2)  # em millisegundos
    
    return Response({
        'string': input_string,
        'vogal': vogal_encontrada,
        'tempoTotal': f"{tempo_total}ms"
    })


def processar_string(texto):
    if not texto or len(texto) < 3:
        return None
    
    vogais = 'aeiouAEIOU'
    
    # Contar frequência de cada caractere para verificar repetição
    contador_chars = {}
    for char in texto:
        if char.lower() in 'aeiou':  # Apenas vogais
            contador_chars[char.lower()] = contador_chars.get(char.lower(), 0) + 1
    
    # Percorrer a string procurando o padrão: vogal -> consoante -> vogal
    for i in range(len(texto) - 2):
        char_anterior = texto[i]
        char_atual = texto[i + 1]
        char_proximo = texto[i + 2]
        
        # Verificar se o padrão é: vogal -> consoante -> vogal
        if (char_anterior in vogais and 
            char_atual not in vogais and 
            char_atual.isalpha() and  # Garantir que é uma letra (consoante)
            char_proximo in vogais):
            
            # Verificar se a vogal (char_proximo) não se repete na string
            if contador_chars.get(char_proximo.lower(), 0) == 1:
                return char_proximo
    
    return None


@extend_schema(
    responses=ExemploUsoSerializer,
    summary="Exemplo de Uso - Desafio Vogal",
    description="Retorna exemplo de como usar a API do desafio vogal com payload e resposta esperada."
)
@api_view(['GET'])
@permission_classes([AllowAny])
def exemplo_uso(request):

    return Response({
        'exemplo': {
            'url': '/api/v1/desafio-vogal/processar/',
            'metodo': 'POST',
            'payload': {
                'string': 'aAbBABacafe'
            },
            'resposta_esperada': {
                'string': 'aAbBABacafe',
                'vogal': 'e',
                'tempoTotal': '10ms'
            }
        },
    })
