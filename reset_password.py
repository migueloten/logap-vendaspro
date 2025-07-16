#!/usr/bin/env python
"""
Script para resetar a senha do usuário admin
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings')
django.setup()

from accounts.models import Usuario

def resetar_senha():
    """Reseta a senha do usuário admin"""
    try:
        usuario = Usuario.objects.get(email='admin@vendaspro.com')
        usuario.set_password('admin123')
        usuario.save()
        print(f"✅ Senha resetada para: admin123")
        print(f"   Email: {usuario.email}")
        print(f"   ID: {usuario.id} (tipo: {type(usuario.id)})")
    except Usuario.DoesNotExist:
        print("❌ Usuário não encontrado")

if __name__ == "__main__":
    resetar_senha()
