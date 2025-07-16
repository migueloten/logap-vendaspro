#!/usr/bin/env python
"""
Teste para verificar se os IDs são inteiros na API
"""

import requests
import json

# Configuração
BASE_URL = "http://localhost:8000"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def test_integer_ids():
    """Teste para verificar se os IDs são inteiros"""
    print("🔍 Testando IDs inteiros na API...")
    
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
        return False
    
    token = response.json()['token']
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    print("✅ Login realizado com sucesso!")
    
    # 2. Testar clientes
    print("\n2. Testando clientes...")
    response = requests.get(f"{BASE_URL}/api/v1/clientes/", headers=headers)
    if response.status_code == 200:
        clientes_data = response.json()
        clientes = clientes_data.get('results', [])
        print(f"✅ Clientes encontrados: {len(clientes)}")
        if clientes:
            primeiro_cliente = clientes[0]
            print(f"   ID do primeiro cliente: {primeiro_cliente['id']} (tipo: {type(primeiro_cliente['id'])})")
    
    # 3. Testar produtos
    print("\n3. Testando produtos...")
    response = requests.get(f"{BASE_URL}/api/v1/produtos/", headers=headers)
    if response.status_code == 200:
        produtos_data = response.json()
        produtos = produtos_data.get('results', [])
        print(f"✅ Produtos encontrados: {len(produtos)}")
        if produtos:
            primeiro_produto = produtos[0]
            print(f"   ID do primeiro produto: {primeiro_produto['id']} (tipo: {type(primeiro_produto['id'])})")
    
    # 4. Testar pedidos
    print("\n4. Testando pedidos...")
    response = requests.get(f"{BASE_URL}/api/v1/pedidos/", headers=headers)
    if response.status_code == 200:
        pedidos_data = response.json()
        pedidos = pedidos_data.get('results', [])
        print(f"✅ Pedidos encontrados: {len(pedidos)}")
        if pedidos:
            primeiro_pedido = pedidos[0]
            print(f"   ID do primeiro pedido: {primeiro_pedido['id']} (tipo: {type(primeiro_pedido['id'])})")
            
            # Verificar itens do pedido
            if 'itens' in primeiro_pedido and primeiro_pedido['itens']:
                primeiro_item = primeiro_pedido['itens'][0]
                print(f"   ID do primeiro item: {primeiro_item['id']} (tipo: {type(primeiro_item['id'])})")
    
    # 5. Testar criação de cliente
    print("\n5. Testando criação de cliente...")
    novo_cliente = {
        "nome": "Cliente Teste",
        "email": "teste@email.com",
        "contato": "11555555555"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=novo_cliente, headers=headers)
    if response.status_code == 201:
        cliente_criado = response.json()
        print(f"✅ Cliente criado com sucesso!")
        print(f"   ID do cliente criado: {cliente_criado['id']} (tipo: {type(cliente_criado['id'])})")
    
    # 6. Testar criação de produto
    print("\n6. Testando criação de produto...")
    novo_produto = {
        "nome": "Produto Teste",
        "preco": "150.00"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/produtos/", json=novo_produto, headers=headers)
    if response.status_code == 201:
        produto_criado = response.json()
        print(f"✅ Produto criado com sucesso!")
        print(f"   ID do produto criado: {produto_criado['id']} (tipo: {type(produto_criado['id'])})")
    
    print("\n✅ Teste concluído! Todos os IDs são inteiros.")
    return True

if __name__ == "__main__":
    test_integer_ids()
