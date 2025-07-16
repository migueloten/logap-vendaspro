# VendasPro - Sistema de Vendas

Sistema completo de vendas desenvolvido em Django com Django REST Framework para gerenciamento de clientes, produtos, pedidos e relatórios empresariais.

**🎯 Inclui API especial**: Desafio Vogal - endpoint que encontra o primeiro caractere vogal após uma consoante antecedida por vogal e que não se repete na string. Funciona enviando uma string via POST e retorna a vogal encontrada com tempo de processamento.

## 🛠️ Tecnologias Utilizadas

### Backend
- **Django 4.2.7** - Framework web Python
- **Django REST Framework 3.14.0** - API REST
- **djangorestframework-simplejwt 5.5.0** - Autenticação JWT
- **django-cors-headers** - CORS para frontend
- **django-filter** - Filtros para API
- **python-decouple** - Configurações de ambiente

### Banco de Dados
- **SQLite** - Desenvolvimento
- **PostgreSQL** - Produção (configurado)

### Autenticação
- **JWT (JSON Web Tokens)** - Autenticação segura
- **Modelo de usuário customizado** - Sistema próprio de usuários

## 🚀 Funcionalidades do Sistema

### 👥 Gestão de Clientes
- Cadastro completo com dados pessoais e endereço
- Listagem e busca de clientes
- Histórico de pedidos por cliente
- Estatísticas automáticas (total de pedidos, valor gasto)

### 📦 Gestão de Produtos
- Cadastro de produtos com categorias
- Controle de estoque
- Preços e disponibilidade
- Busca e filtros avançados

### 🛒 Sistema de Pedidos
- Criação de pedidos com múltiplos itens
- Status de acompanhamento (Pendente → Em Andamento → Finalizado → Cancelado)
- Cálculo automático de totais
- Histórico completo de alterações

### 📊 Relatórios e Dashboard
- Dashboard com métricas gerais
- Relatórios de vendas por período
- Clientes mais ativos
- Pedidos pendentes
- Estatísticas de faturamento

### 🔐 Sistema de Autenticação
- Login seguro com JWT
- Controle de acesso por usuário
- Tokens de acesso e refresh
- Logout com blacklist de tokens

## 🌐 API REST

### Endpoints Principais

**Autenticação**
- `POST /api/v1/auth/login/` - Login do usuário
- `POST /api/v1/auth/logout/` - Logout
- `GET /api/v1/auth/profile/` - Perfil do usuário
- `POST /api/v1/auth/verify/` - Verificar token

**Clientes**
- `GET/POST /api/v1/clientes/` - Listar/Criar clientes
- `GET/PUT/DELETE /api/v1/clientes/{id}/` - Operações específicas

**Produtos**
- `GET/POST /api/v1/produtos/` - Listar/Criar produtos
- `GET/POST /api/v1/categorias/` - Gerenciar categorias

**Pedidos**
- `GET/POST /api/v1/pedidos/` - Listar/Criar pedidos
- `GET/PUT/DELETE /api/v1/pedidos/{id}/` - Operações específicas

**Relatórios**
- `GET /api/v1/relatorios/geral/` - Dashboard geral
- `GET /api/v1/relatorios/clientes-ativos/` - Clientes mais ativos
- `GET /api/v1/relatorios/pedidos-pendentes/` - Pedidos pendentes

**Desafio Vogal**
- `POST /api/v1/desafio-vogal/processar/` - Processa string e encontra vogal especial
- `GET /api/v1/desafio-vogal/exemplo/` - Exemplo de uso da API

## � Como Executar

### 1. Instalação
```bash
# Clonar o repositório
git clone <url-do-repositorio>
cd django-vendaspro

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configuração
```bash
# Aplicar migrações
python manage.py migrate

# Popular dados de teste
python manage.py popular_dados_teste

# Executar servidor
python manage.py runserver
```

### 3. Acesso
- **Servidor**: http://localhost:8000/
- **Admin Django**: http://localhost:8000/admin/

## 🔐 Credenciais de Acesso

**Email:** admin@vendaspro.com  
**Senha:** 123456

## 📁 Estrutura do Projeto

```
django-vendaspro/
├── accounts/          # Autenticação e usuários
├── clientes/          # Gestão de clientes
├── produtos/          # Produtos e categorias
├── pedidos/           # Sistema de pedidos
├── core/              # Relatórios e dashboard
├── vendaspro/         # Configurações do Django
├── manage.py          # Comando principal do Django
└── requirements.txt   # Dependências do projeto
```

## 🎯 Características Técnicas

### Segurança
- Autenticação JWT com refresh tokens
- Validação de dados em todas as operações
- Controle de acesso por usuário

### Performance
- Queries otimizadas com select_related
- Paginação automática nas listagens
- Índices no banco de dados

### Flexibilidade
- API REST completa
- Configurações por ambiente
- Estrutura modular

### Manutenção
- Código bem documentado
- Testes unitários
- Logs de operações

## 📈 Próximas Melhorias

- Interface web (React/Vue.js)
- Relatórios em PDF/Excel
- Sistema de notificações
- Integração com pagamentos
- App mobile
- Dashboard em tempo real
