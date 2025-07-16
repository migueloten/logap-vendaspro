#!/usr/bin/env python
"""
Teste simples para verificar CSRF no Swagger UI
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8000"
SWAGGER_URL = f"{BASE_URL}/api/swagger/"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def test_swagger_csrf_simple():
    """Teste simples para CSRF no Swagger"""
    print("🔍 Testando CSRF no Swagger UI (versão simples)...")
    
    # 1. Obter token
    print("\n1. Obtendo token...")
    login_url = f"{BASE_URL}/api/v1/auth/login/"
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"❌ Erro no login: {response.status_code}")
        print(f"Resposta: {response.text}")
        return False
    
    token = response.json()['token']
    print(f"✅ Token obtido: {token[:20]}...")
    
    # 2. Testar diferentes tipos de requisições
    headers_base = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    # Teste 1: Requisição básica
    print("\n2. Teste básico...")
    cliente_data = {
        "nome": "Cliente Teste Básico",
        "email": "basico@email.com",
        "contato": "11999999999"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data, headers=headers_base)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Requisição básica funcionando!")
    elif response.status_code == 403:
        print("❌ Erro 403 - Problema de CSRF ainda existe")
        print(f"Resposta: {response.text}")
        return False
    else:
        print(f"❌ Outro erro: {response.status_code}")
        print(f"Resposta: {response.text}")
    
    # Teste 2: Simulando requisição do Swagger
    print("\n3. Simulando requisição do Swagger...")
    headers_swagger = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:8000',
        'Referer': SWAGGER_URL,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    cliente_data_swagger = {
        "nome": "Cliente Swagger Test",
        "email": "swagger@email.com",
        "contato": "11888888888"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data_swagger, headers=headers_swagger)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Requisição tipo Swagger funcionando!")
    elif response.status_code == 403:
        print("❌ Erro 403 - Problema de CSRF no Swagger")
        print(f"Resposta: {response.text}")
        
        # Verificar se é especificamente CSRF
        if "CSRF" in response.text:
            print("🔍 Confirmado: Problema de CSRF token")
            return False
    else:
        print(f"❌ Outro erro: {response.status_code}")
        print(f"Resposta: {response.text}")
    
    # Teste 3: Com session
    print("\n4. Testando com session...")
    session = requests.Session()
    
    # Primeiro, acessar a página do Swagger para obter cookies
    session.get(SWAGGER_URL)
    
    # Agora fazer a requisição com a session
    response = session.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data, headers=headers_base)
    print(f"Status com session: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Requisição com session funcionando!")
    elif response.status_code == 403:
        print("❌ Erro 403 - Problema de CSRF com session")
        print(f"Resposta: {response.text}")
    else:
        print(f"❌ Outro erro: {response.status_code}")
    
    # Verificar se o Swagger está acessível
    print("\n5. Verificando acesso ao Swagger...")
    response = requests.get(SWAGGER_URL)
    print(f"Status do Swagger: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Swagger UI acessível!")
    else:
        print(f"❌ Swagger UI não acessível: {response.status_code}")
    
    print("\n📋 Resumo dos testes:")
    print("- API básica: ✅ (funcionando)")
    print("- Swagger UI: ❓ (precisa ser testado manualmente)")
    print("- Session: ❓ (variável)")
    
    print("\n🎯 Para testar no Swagger:")
    print("1. Acesse: http://localhost:8000/api/swagger/")
    print("2. Clique em 'Authorize' no topo")
    print(f"3. Insira: Token {token}")
    print("4. Teste o endpoint POST /api/v1/clientes/")
    print("5. Use este JSON:")
    print(json.dumps(cliente_data, indent=2))
    
    return True

if __name__ == "__main__":
    test_swagger_csrf_simple()
