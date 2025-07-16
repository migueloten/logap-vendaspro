import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings.development')
django.setup()

from django.contrib.auth import authenticate
from accounts.models import Usuario

print("=== TESTE DE AUTENTICAÇÃO ===")

# Testar login com email
user = authenticate(username='admin@vendaspro.com', password='admin123')
if user:
    print("✅ Login com admin@vendaspro.com funcionou!")
    print(f"Usuário: {user.username} ({user.email})")
else:
    print("❌ Falha no login com admin@vendaspro.com")

# Testar login com o primeiro usuário
user2 = authenticate(username='admin@admin.com', password='admin123')
if user2:
    print("✅ Login com admin@admin.com funcionou!")
    print(f"Usuário: {user2.username} ({user2.email})")
else:
    print("❌ Falha no login com admin@admin.com")

# Testar se o usuário existe e tem as permissões corretas
try:
    user_obj = Usuario.objects.get(email='admin@vendaspro.com')
    print(f"\n📝 Dados do usuário admin@vendaspro.com:")
    print(f"Username: {user_obj.username}")
    print(f"Email: {user_obj.email}")
    print(f"Is_staff: {user_obj.is_staff}")
    print(f"Is_superuser: {user_obj.is_superuser}")
    print(f"Is_active: {user_obj.is_active}")
    print(f"Has_usable_password: {user_obj.has_usable_password()}")
except Usuario.DoesNotExist:
    print("❌ Usuário admin@vendaspro.com não encontrado")
