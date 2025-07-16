#!/usr/bin/env python
"""
Script para criar superusuário com campos inteiros
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings')
django.setup()

from accounts.models import Usuario

def criar_superusuario():
    """Cria superusuário com ID inteiro"""
    email = 'admin@vendaspro.com'
    nome = 'Administrador'
    senha = 'admin123'
    
    # Verificar se usuário já existe
    if Usuario.objects.filter(email=email).exists():
        print(f"Usuário {email} já existe!")
        usuario = Usuario.objects.get(email=email)
        print(f"ID do usuário: {usuario.id} (tipo: {type(usuario.id)})")
        return usuario
    
    # Criar superusuário
    usuario = Usuario.objects.create_superuser(
        email=email,
        nome=nome,
        password=senha
    )
    
    print(f"Superusuário criado com sucesso!")
    print(f"Email: {usuario.email}")
    print(f"Nome: {usuario.nome}")
    print(f"ID: {usuario.id} (tipo: {type(usuario.id)})")
    print(f"É admin: {usuario.is_admin}")
    print(f"É staff: {usuario.is_staff}")
    print(f"É superusuário: {usuario.is_superuser}")
    
    return usuario

if __name__ == "__main__":
    criar_superusuario()
