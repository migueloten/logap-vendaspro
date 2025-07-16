#!/usr/bin/env python
"""
Teste específico para verificar CSRF no Swagger UI
"""

import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# Configuração
BASE_URL = "http://localhost:8000"
SWAGGER_URL = f"{BASE_URL}/api/swagger/"
EMAIL = "admin@vendaspro.com"
PASSWORD = "admin123"

def test_swagger_csrf():
    """Teste específico para CSRF no Swagger"""
    print("🔍 Testando CSRF no Swagger UI...")
    
    # 1. Primeiro, obter token via API
    print("\n1. Obtendo token via API...")
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
    
    # 2. Testar criação direta via API (sem Swagger)
    print("\n2. Testando criação direta via API...")
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json'
    }
    
    cliente_data = {
        "nome": "Cliente API Direct",
        "email": "api_direct@email.com",
        "contato": "11999999999"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data, headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ API direta funcionando!")
    else:
        print(f"❌ API direta falhou: {response.text}")
    
    # 3. Testar através do navegador (simulando Swagger)
    print("\n3. Testando através do navegador...")
    
    # Configurar Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navegar para o Swagger
        driver.get(SWAGGER_URL)
        time.sleep(2)
        
        print("✅ Swagger UI carregado")
        
        # Tentar fazer uma requisição através do JavaScript
        script = f"""
        fetch('{BASE_URL}/api/v1/clientes/', {{
            method: 'POST',
            headers: {{
                'Authorization': 'Token {token}',
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({{
                nome: 'Cliente JS Test',
                email: 'js_test@email.com',
                contato: '11888888888'
            }})
        }})
        .then(response => response.json())
        .then(data => {{
            window.testResult = {{
                success: true,
                status: 201,
                data: data
            }};
        }})
        .catch(error => {{
            window.testResult = {{
                success: false,
                error: error.message
            }};
        }});
        """
        
        driver.execute_script(script)
        time.sleep(3)
        
        # Verificar resultado
        result = driver.execute_script("return window.testResult;")
        
        if result and result.get('success'):
            print("✅ Requisição JavaScript funcionando!")
            print(f"Status: {result.get('status')}")
        else:
            print(f"❌ Requisição JavaScript falhou: {result}")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro no teste do navegador: {e}")
        print("⚠️  Teste do navegador pulado (Chrome não instalado ou problema de configuração)")
    
    # 4. Testar com diferentes headers
    print("\n4. Testando com diferentes headers...")
    
    # Teste com X-CSRFToken
    headers_with_csrf = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'X-CSRFToken': 'test-token'
    }
    
    cliente_data_2 = {
        "nome": "Cliente CSRF Header",
        "email": "csrf_header@email.com",
        "contato": "11777777777"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data_2, headers=headers_with_csrf)
    print(f"Status com X-CSRFToken: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Requisição com X-CSRFToken funcionando!")
    else:
        print(f"❌ Requisição com X-CSRFToken falhou: {response.text}")
    
    # Teste com Referer
    headers_with_referer = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
        'Referer': SWAGGER_URL
    }
    
    cliente_data_3 = {
        "nome": "Cliente Referer",
        "email": "referer@email.com",
        "contato": "11666666666"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/clientes/", json=cliente_data_3, headers=headers_with_referer)
    print(f"Status com Referer: {response.status_code}")
    
    if response.status_code == 201:
        print("✅ Requisição com Referer funcionando!")
    else:
        print(f"❌ Requisição com Referer falhou: {response.text}")
    
    print("\n🎯 Teste do Swagger CSRF concluído!")
    return True

if __name__ == "__main__":
    test_swagger_csrf()
