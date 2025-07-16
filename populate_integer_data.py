#!/usr/bin/env python
"""
Script para criar dados de teste com IDs inteiros
"""
import os
import sys
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings')
django.setup()

from clientes.models import Cliente
from produtos.models import Produto
from pedidos.models import Pedido, PedidoItem
from accounts.models import Usuario

def criar_dados_teste():
    """Cria dados de teste com IDs inteiros"""
    
    # 1. Criar clientes
    print("=== CRIANDO CLIENTES ===")
    clientes = [
        {'nome': 'João Silva', 'email': 'joao@email.com', 'contato': '11999999999'},
        {'nome': 'Maria Santos', 'email': 'maria@email.com', 'contato': '11888888888'},
        {'nome': 'Pedro Oliveira', 'email': 'pedro@email.com', 'contato': '11777777777'},
        {'nome': 'Ana Costa', 'email': 'ana@email.com', 'contato': '11666666666'},
    ]
    
    for cliente_data in clientes:
        cliente = Cliente.objects.create(**cliente_data)
        print(f"Cliente criado: {cliente.nome} - ID: {cliente.id} (tipo: {type(cliente.id)})")
    
    # 2. Criar produtos
    print("\n=== CRIANDO PRODUTOS ===")
    produtos = [
        {'nome': 'Notebook Dell', 'preco': Decimal('2500.00')},
        {'nome': 'Mouse Logitech', 'preco': Decimal('89.90')},
        {'nome': 'Teclado Mecânico', 'preco': Decimal('299.99')},
        {'nome': 'Monitor 24"', 'preco': Decimal('899.00')},
        {'nome': 'Webcam HD', 'preco': Decimal('199.50')},
    ]
    
    for produto_data in produtos:
        produto = Produto.objects.create(**produto_data)
        print(f"Produto criado: {produto.nome} - ID: {produto.id} (tipo: {type(produto.id)})")
    
    # 3. Criar pedidos
    print("\n=== CRIANDO PEDIDOS ===")
    cliente1 = Cliente.objects.get(email='joao@email.com')
    cliente2 = Cliente.objects.get(email='maria@email.com')
    
    produto1 = Produto.objects.get(nome='Notebook Dell')
    produto2 = Produto.objects.get(nome='Mouse Logitech')
    produto3 = Produto.objects.get(nome='Teclado Mecânico')
    
    # Pedido 1
    pedido1 = Pedido.objects.create(
        cliente=cliente1,
        endereco_cep='01234-567',
        endereco_cidade='São Paulo',
        endereco_uf='SP',
        endereco_rua='Rua das Flores, 123',
        endereco_numero='123',
        endereco_complemento='Apto 45',
        frete=Decimal('25.00'),
        total=Decimal('2614.90')  # Notebook + Mouse + Frete
    )
    print(f"Pedido criado: {pedido1.numero} - ID: {pedido1.id} (tipo: {type(pedido1.id)})")
    
    # Itens do pedido 1
    item1 = PedidoItem.objects.create(
        pedido=pedido1,
        produto=produto1,
        quantidade=1,
        preco_unitario=produto1.preco
    )
    print(f"Item criado: {item1.produto.nome} - ID: {item1.id} (tipo: {type(item1.id)})")
    
    item2 = PedidoItem.objects.create(
        pedido=pedido1,
        produto=produto2,
        quantidade=1,
        preco_unitario=produto2.preco
    )
    print(f"Item criado: {item2.produto.nome} - ID: {item2.id} (tipo: {type(item2.id)})")
    
    # Pedido 2
    pedido2 = Pedido.objects.create(
        cliente=cliente2,
        endereco_cep='04567-890',
        endereco_cidade='Rio de Janeiro',
        endereco_uf='RJ',
        endereco_rua='Av. Brasil, 456',
        endereco_numero='456',
        endereco_complemento='',
        frete=Decimal('35.00'),
        total=Decimal('334.99')  # Teclado + Frete
    )
    print(f"Pedido criado: {pedido2.numero} - ID: {pedido2.id} (tipo: {type(pedido2.id)})")
    
    # Item do pedido 2
    item3 = PedidoItem.objects.create(
        pedido=pedido2,
        produto=produto3,
        quantidade=1,
        preco_unitario=produto3.preco
    )
    print(f"Item criado: {item3.produto.nome} - ID: {item3.id} (tipo: {type(item3.id)})")
    
    # 4. Verificar usuário
    print("\n=== VERIFICANDO USUÁRIO ===")
    usuario = Usuario.objects.first()
    print(f"Usuário: {usuario.email} - ID: {usuario.id} (tipo: {type(usuario.id)})")
    
    # 5. Resumo
    print("\n=== RESUMO ===")
    print(f"Total de clientes: {Cliente.objects.count()}")
    print(f"Total de produtos: {Produto.objects.count()}")
    print(f"Total de pedidos: {Pedido.objects.count()}")
    print(f"Total de itens de pedidos: {PedidoItem.objects.count()}")
    print(f"Total de usuários: {Usuario.objects.count()}")
    
    # Verificar se todos os IDs são inteiros
    print("\n=== VERIFICAÇÃO DE TIPOS ===")
    print(f"Todos os IDs são inteiros:")
    
    for cliente in Cliente.objects.all():
        print(f"  Cliente {cliente.id}: {type(cliente.id).__name__}")
    
    for produto in Produto.objects.all():
        print(f"  Produto {produto.id}: {type(produto.id).__name__}")
    
    for pedido in Pedido.objects.all():
        print(f"  Pedido {pedido.id}: {type(pedido.id).__name__}")
    
    for item in PedidoItem.objects.all():
        print(f"  Item {item.id}: {type(item.id).__name__}")
    
    for usuario in Usuario.objects.all():
        print(f"  Usuário {usuario.id}: {type(usuario.id).__name__}")
    
    print("\n✅ Dados de teste criados com sucesso!")

if __name__ == "__main__":
    criar_dados_teste()
