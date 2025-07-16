from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario, TokenCustom

class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'ativo')
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Credenciais inválidas.')
            
            if not user.ativo:
                raise serializers.ValidationError('Usuário inativo.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Email e senha são obrigatórios.')

class TokenCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenCustom
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
