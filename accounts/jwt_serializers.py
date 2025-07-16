from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from .models import Usuario


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado para obter tokens JWT
    """
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.EmailField()
        self.fields['password'] = serializers.CharField()
        # Remove o campo username padrão
        if 'username' in self.fields:
            del self.fields['username']
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Adicionar claims personalizados
        token['email'] = user.email
        token['nome'] = f"{user.first_name} {user.last_name}".strip()
        token['is_admin'] = user.is_staff
        
        return token
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Credenciais inválidas.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'Conta de usuário desativada.',
                    code='authorization'
                )
            
            refresh = self.get_token(user)
            
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UsuarioSerializer(user).data
            }
        else:
            raise serializers.ValidationError(
                'É necessário fornecer email e senha.',
                code='authorization'
            )


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para dados do usuário
    """
    nome = serializers.SerializerMethodField()
    
    class Meta:
        model = Usuario
        fields = ['id', 'email', 'nome', 'is_staff', 'is_superuser', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_nome(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.email
