from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiExample
from .serializers import LoginSerializer, UsuarioSerializer

class CustomAuthToken(ObtainAuthToken):
    """
    Custom token obtain view para compatibilidade
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

# Instância da view personalizada
obtain_auth_token = CustomAuthToken.as_view()

@extend_schema(
    tags=['Autenticação'],
    summary='Login de usuário',
    description='Endpoint para autenticação de usuários. Retorna um token de acesso.',
    request=LoginSerializer,
    examples=[
        OpenApiExample(
            'Login admin',
            value={
                'email': 'admin@vendaspro.com',
                'password': 'admin123'
            }
        )
    ],
    responses={
        200: {
            'description': 'Login realizado com sucesso',
            'examples': {
                'application/json': {
                    'token': 'abcd1234efgh5678ijkl90mnop',
                    'user': {
                        'id': '123e4567-e89b-12d3-a456-426614174000',
                        'email': 'admin@vendaspro.com',
                        'first_name': 'Admin',
                        'last_name': 'VendasPro'
                    },
                    'expires_in': 86400
                }
            }
        },
        400: {
            'description': 'Credenciais inválidas'
        }
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    """
    Endpoint para login de usuários
    """
    serializer = LoginSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Criar ou obter token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'expires_in': 86400  # 24 horas
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=['Autenticação'],
    summary='Logout de usuário',
    description='Endpoint para logout de usuários. Remove o token de acesso.',
    responses={
        200: {
            'description': 'Logout realizado com sucesso',
            'examples': {
                'application/json': {
                    'message': 'Logout realizado com sucesso'
                }
            }
        },
        400: {
            'description': 'Erro no logout'
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def logout_view(request):
    """
    Endpoint para logout de usuários
    """
    try:
        # Remover token do usuário
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Endpoint para obter perfil do usuário logado
    """
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    Endpoint para registro de novos usuários
    """
    serializer = UsuarioSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Criar token automaticamente
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UsuarioSerializer(user).data,
            'token': token.key,
            'message': 'Usuário criado com sucesso'
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
