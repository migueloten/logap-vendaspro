import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings.development')
django.setup()

from accounts.models import Usuario

# Criar usuário correto
try:
    user = Usuario.objects.create_user(
        username='admin_vendas',
        email='admin@vendaspro.com',
        password='admin123',
        first_name='Admin',
        last_name='VendasPro'
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("✅ Usuário admin@vendaspro.com criado com sucesso!")
    print("Email: admin@vendaspro.com")
    print("Senha: admin123")
except Exception as e:
    print(f"Erro: {e}")
    
# Listar todos os usuários
print("\n=== TODOS OS USUÁRIOS ===")
for user in Usuario.objects.all():
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is_staff: {user.is_staff}")
    print(f"Is_superuser: {user.is_superuser}")
    print("---")
