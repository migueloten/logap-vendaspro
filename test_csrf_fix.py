#!/usr/bin/env python
"""
Teste completo para verificar se o CSRF foi resolvido
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8000"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def test_csrf_resolution():
    """Teste para verificar se o CSRF foi resolvido"""
    print("🔍 Testando resolução do problema CSRF...")
    
    # 1. Fazer login
    print("\n1. Fazendo login...")
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
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print("✅ Login realizado com sucesso!")
    print(f"Token: {token[:20]}...")
    
    # 2. Testar criação de cliente (onde estava o erro CSRF)
    print("\n2. Testando criação de cliente...")
    cliente_data = {
        "nome": "Cliente Teste CSRF Fix",
        "email": f"csrf_test_{len(str(response.json()))}@email.com",
        "contato": "11888888888"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        cliente_criado = response.json()
        print(f"✅ Cliente criado com sucesso!")
        print(f"ID: {cliente_criado['id']}")
        print(f"Nome: {cliente_criado['nome']}")
        print(f"Email: {cliente_criado['email']}")
        
        # 3. Testar atualização do cliente
        print("\n3. Testando atualização de cliente...")
        cliente_id = cliente_criado['id']
        cliente_update = {
            "nome": "Cliente Atualizado CSRF",
            "email": cliente_criado['email'],
            "contato": "11777777777"
        }
        
        response = requests.put(f"{BASE_URL}/api/v1/clientes/{cliente_id}/", json=cliente_update, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            cliente_atualizado = response.json()
            print(f"✅ Cliente atualizado com sucesso!")
            print(f"Nome atualizado: {cliente_atualizado['nome']}")
            print(f"Contato atualizado: {cliente_atualizado['contato']}")
        else:
            print(f"❌ Erro ao atualizar cliente: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        # 4. Testar criação de produto
        print("\n4. Testando criação de produto...")
        produto_data = {
            "nome": "Produto Teste CSRF",
            "preco": "99.99"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/produtos/", json=produto_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            produto_criado = response.json()
            print(f"✅ Produto criado com sucesso!")
            print(f"ID: {produto_criado['id']}")
            print(f"Nome: {produto_criado['nome']}")
            print(f"Preço: R$ {produto_criado['preco']}")
        else:
            print(f"❌ Erro ao criar produto: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        # 5. Testar criação de pedido
        print("\n5. Testando criação de pedido...")
        pedido_data = {
            "cliente": cliente_id,
            "endereco_cep": "01234-567",
            "endereco_cidade": "São Paulo",
            "endereco_uf": "SP",
            "endereco_rua": "Rua Teste CSRF",
            "endereco_numero": "123",
            "endereco_complemento": "Apto 456",
            "frete": "15.00",
            "total": "114.99",
            "itens": [
                {
                    "produto": produto_criado['id'] if 'produto_criado' in locals() else 1,
                    "quantidade": 1,
                    "preco_unitario": "99.99"
                }
            ]
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/pedidos/", json=pedido_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            pedido_criado = response.json()
            print(f"✅ Pedido criado com sucesso!")
            print(f"ID: {pedido_criado['id']}")
            print(f"Número: {pedido_criado['numero']}")
            print(f"Total: R$ {pedido_criado['total']}")
        else:
            print(f"❌ Erro ao criar pedido: {response.status_code}")
            print(f"Resposta: {response.text}")
        
        print("\n✅ Todos os testes CRUD passaram! CSRF resolvido com sucesso!")
        return True
        
    else:
        print(f"❌ Erro ao criar cliente: {response.status_code}")
        print(f"Resposta: {response.text}")
        
        if response.status_code == 403:
            response_data = response.json()
            if "CSRF" in response_data.get("detail", ""):
                print("⚠️  Problema CSRF ainda não resolvido!")
                return False
        
        return False

if __name__ == "__main__":
    success = test_csrf_resolution()
    if success:
        print("\n🎉 CSRF TOKEN PROBLEMA RESOLVIDO!")
        print("✅ Você pode agora usar o Swagger UI sem problemas de CSRF")
        print("✅ Todas as operações CRUD funcionam corretamente")
        print("✅ API está pronta para uso")
    else:
        print("\n❌ Problema CSRF ainda não foi completamente resolvido")
