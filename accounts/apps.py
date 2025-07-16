from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Contas de Usuário'
    
    def ready(self):
        # Importar signals quando o app estiver pronto
        try:
            import accounts.signals
        except ImportError:
            pass
