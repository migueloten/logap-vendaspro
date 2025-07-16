#!/usr/bin/env python
"""
Teste para verificar se a autenticação do Swagger está funcionando
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8000"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def test_swagger_authentication():
    """Teste completo da autenticação no Swagger"""
    print("🔍 Testando autenticação no Swagger...")
    
    # 1. Fazer login e obter token
    print("\n1. Fazendo login...")
    login_url = f"{BASE_URL}/api/v1/auth/login/"
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(login_url, json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token')
        user_data = data.get('user', {})
        
        print(f"   ✅ Login realizado com sucesso!")
        print(f"   Token: {token[:20]}...")
        print(f"   Usuário: {user_data.get('nome', 'N/A')} ({user_data.get('email', 'N/A')})")
        
        # 2. Testar endpoint protegido
        print("\n2. Testando endpoint protegido com token...")
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        # Testar endpoint de clientes
        clientes_url = f"{BASE_URL}/api/v1/clientes/"
        response = requests.get(clientes_url, headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            clientes = response.json()
            print(f"   ✅ Endpoint protegido acessível!")
            print(f"   Clientes encontrados: {len(clientes)}")
        else:
            print(f"   ❌ Erro ao acessar endpoint protegido")
            print(f"   Resposta: {response.text}")
            
        # 3. Verificar schema do Swagger
        print("\n3. Verificando schema do OpenAPI...")
        schema_url = f"{BASE_URL}/api/schema/"
        response = requests.get(schema_url)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                schema = response.json()
                print(f"   ✅ Schema OpenAPI disponível!")
                print(f"   Título: {schema.get('info', {}).get('title', 'N/A')}")
                print(f"   Versão: {schema.get('info', {}).get('version', 'N/A')}")
                
                # Verificar se tem configuração de segurança
                if 'components' in schema and 'securitySchemes' in schema['components']:
                    security_schemes = schema['components']['securitySchemes']
                    print(f"   Esquemas de segurança: {list(security_schemes.keys())}")
            except Exception as e:
                print(f"   ❌ Erro ao processar schema: {e}")
                print(f"   Resposta: {response.text[:200]}...")
        else:
            print(f"   ❌ Erro ao acessar schema: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}...")
            
        return True
        
    else:
        print(f"   ❌ Erro no login: {response.status_code}")
        print(f"   Resposta: {response.text}")
        return False

if __name__ == "__main__":
    test_swagger_authentication()
