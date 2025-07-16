import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vendaspro.settings.development')
django.setup()

from accounts.models import Usuario

print("=== USUÁRIOS NO BANCO ===")
for user in Usuario.objects.all():
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is_staff: {user.is_staff}")
    print(f"Is_superuser: {user.is_superuser}")
    print(f"Is_active: {user.is_active}")
    print("---")

print(f"Total de usuários: {Usuario.objects.count()}")
