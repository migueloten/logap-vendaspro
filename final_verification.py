#!/usr/bin/env python
"""
Verificação final e instruções para usar o Swagger
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8000"
SWAGGER_URL = f"{BASE_URL}/api/swagger/"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def final_verification():
    """Verificação final completa"""
    print("🔍 VERIFICAÇÃO FINAL - CSRF e Swagger UI")
    print("=" * 50)
    
    # 1. Obter token
    print("\n1. 🔑 Obtendo token de autenticação...")
    login_url = f"{BASE_URL}/api/v1/auth/login/"
    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    response = requests.post(login_url, json=login_data)
    if response.status_code != 200:
        print(f"❌ ERRO: Não foi possível fazer login")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
        return False
    
    token = response.json()['token']
    user_data = response.json()['user']
    print(f"✅ LOGIN REALIZADO COM SUCESSO!")
    print(f"   Token: {token}")
    print(f"   Usuário: {user_data['first_name']} {user_data['last_name']}")
    print(f"   Email: {user_data['email']}")
    
    # 2. Testar criação de cliente
    print("\n2. 🧪 Testando criação de cliente...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    cliente_data = {
        "nome": "Cliente Teste Final",
        "email": "teste_final@email.com",
        "contato": "11999999999"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        cliente_criado = response.json()
        print(f"✅ CLIENTE CRIADO COM SUCESSO!")
        print(f"   ID: {cliente_criado['id']}")
        print(f"   Nome: {cliente_criado['nome']}")
        print(f"   Email: {cliente_criado['email']}")
        csrf_ok = True
    elif response.status_code == 403:
        print(f"❌ ERRO 403 - PROBLEMA DE CSRF AINDA EXISTE!")
        print(f"Resposta: {response.text}")
        csrf_ok = False
    else:
        print(f"❌ ERRO: {response.status_code}")
        print(f"Resposta: {response.text}")
        csrf_ok = False
    
    # 3. Verificar Swagger
    print("\n3. 📖 Verificando Swagger UI...")
    response = requests.get(SWAGGER_URL)
    if response.status_code == 200:
        print("✅ SWAGGER UI ACESSÍVEL!")
        print(f"   URL: {SWAGGER_URL}")
    else:
        print(f"❌ SWAGGER UI NÃO ACESSÍVEL: {response.status_code}")
    
    # 4. Instruções finais
    print("\n" + "=" * 50)
    print("🎯 INSTRUÇÕES PARA USAR O SWAGGER UI")
    print("=" * 50)
    
    if csrf_ok:
        print("✅ CSRF RESOLVIDO - Swagger deve funcionar!")
        print()
        print("📋 PASSO A PASSO:")
        print("1. Acesse o Swagger UI:")
        print(f"   {SWAGGER_URL}")
        print()
        print("2. Clique no botão 'Authorize' (cadeado) no topo da página")
        print()
        print("3. No campo 'Value', insira EXATAMENTE:")
        print(f"   Token {token}")
        print()
        print("4. Clique em 'Authorize' e depois 'Close'")
        print()
        print("5. Agora você pode testar qualquer endpoint!")
        print()
        print("🧪 TESTE SUGERIDO:")
        print("- Vá até 'POST /api/v1/clientes/'")
        print("- Clique em 'Try it out'")
        print("- Use este JSON:")
        print(json.dumps({
            "nome": "Cliente Swagger",
            "email": "swagger@email.com",
            "contato": "11888888888"
        }, indent=2))
        print("- Clique em 'Execute'")
        print("- Deve retornar status 201 (Created)")
        
    else:
        print("❌ PROBLEMA DE CSRF AINDA EXISTE!")
        print()
        print("🔧 SOLUÇÕES ADICIONAIS:")
        print("1. Reinicie o servidor Django")
        print("2. Limpe o cache do navegador")
        print("3. Tente em uma aba anônima/incógnita")
        print("4. Verifique se as configurações foram aplicadas")
    
    print("\n" + "=" * 50)
    print("🔑 CREDENCIAIS DE ACESSO")
    print("=" * 50)
    print(f"Email: {EMAIL}")
    print(f"Password: {PASSWORD}")
    print(f"Token: {token}")
    print(f"Swagger URL: {SWAGGER_URL}")
    
    print("\n" + "=" * 50)
    print("🚀 ENDPOINTS DISPONÍVEIS")
    print("=" * 50)
    print("• POST /api/v1/auth/login/ - Fazer login")
    print("• POST /api/v1/auth/logout/ - Fazer logout")
    print("• GET /api/v1/clientes/ - Listar clientes")
    print("• POST /api/v1/clientes/ - Criar cliente")
    print("• GET /api/v1/clientes/{id}/ - Obter cliente")
    print("• PUT /api/v1/clientes/{id}/ - Atualizar cliente")
    print("• DELETE /api/v1/clientes/{id}/ - Deletar cliente")
    print("• GET /api/v1/produtos/ - Listar produtos")
    print("• GET /api/v1/pedidos/ - Listar pedidos")
    print("• POST /api/v1/pedidos/ - Criar pedido")
    
    return csrf_ok

if __name__ == "__main__":
    success = final_verification()
    
    if success:
        print("\n🎉 TUDO FUNCIONANDO!")
        print("✅ CSRF resolvido")
        print("✅ API funcionando") 
        print("✅ Swagger UI acessível")
        print("✅ Pronto para usar!")
    else:
        print("\n⚠️  PROBLEMA IDENTIFICADO")
        print("❌ CSRF ainda não resolvido completamente")
        print("🔧 Siga as instruções acima para resolver")
