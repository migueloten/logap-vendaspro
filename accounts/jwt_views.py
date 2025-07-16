from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, OpenApiExample
from .jwt_serializers import (
    CustomTokenObtainPairSerializer, 
    UsuarioSerializer
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Endpoint para login JWT
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    @extend_schema(
        tags=['Autenticação'],
        summary='Login JWT',
        description='Endpoint para autenticação JWT. Retorna access e refresh tokens.',
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
                        'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                        'user': {
                            'id': 1,
                            'email': 'admin@vendaspro.com',
                            'nome': 'Administrador',
                            'is_staff': True,
                            'is_superuser': True
                        }
                    }
                }
            },
            400: {
                'description': 'Credenciais inválidas'
            }
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


@extend_schema(
    tags=['Autenticação'],
    summary='Logout JWT',
    description='Endpoint para logout JWT. Adiciona refresh token à blacklist.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {
                    'type': 'string',
                    'description': 'Refresh token para blacklist'
                }
            }
        }
    },
    responses={
        200: {
            'description': 'Logout realizado com sucesso'
        },
        400: {
            'description': 'Token inválido'
        }
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def logout_view(request):
    """
    Endpoint para logout JWT
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        logout(request)
        return Response({'message': 'Logout realizado com sucesso'}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Autenticação'],
    summary='Perfil do usuário',
    description='Endpoint para obter informações do usuário autenticado.',
    responses={
        200: {
            'description': 'Dados do usuário',
            'examples': {
                'application/json': {
                    'id': 1,
                    'email': 'admin@vendaspro.com',
                    'nome': 'Administrador',
                    'is_staff': True,
                    'is_superuser': True,
                    'date_joined': '2025-01-01T00:00:00Z'
                }
            }
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Endpoint para obter perfil do usuário autenticado
    """
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)


@extend_schema(
    tags=['Autenticação'],
    summary='Verificar token JWT',
    description='Endpoint para verificar se o token JWT é válido.',
    responses={
        200: {
            'description': 'Token válido',
            'examples': {
                'application/json': {
                    'valid': True,
                    'user': {
                        'id': 1,
                        'email': 'admin@vendaspro.com',
                        'nome': 'Administrador'
                    }
                }
            }
        },
        401: {
            'description': 'Token inválido'
        }
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Endpoint para verificar se o token JWT é válido
    """
    serializer = UsuarioSerializer(request.user)
    return Response({
        'valid': True,
        'user': serializer.data
    })
