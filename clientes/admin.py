from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'contato', 'total_pedidos', 'valor_total_gasto', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('nome', 'email', 'contato')
    readonly_fields = ('total_pedidos', 'valor_total_gasto', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'email', 'contato')
        }),
        ('Estatísticas', {
            'fields': ('total_pedidos', 'valor_total_gasto'),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        # Mostrar todos os clientes, incluindo os deletados
        return Cliente.objects.all()
    
    actions = ['reativar_clientes', 'atualizar_estatisticas']
    
    def reativar_clientes(self, request, queryset):
        """Action para reativar clientes selecionados"""
        updated = queryset.update(deleted_at=None, ativo=True)
        self.message_user(request, f'{updated} clientes reativados com sucesso.')
    reativar_clientes.short_description = "Reativar clientes selecionados"
    
    def atualizar_estatisticas(self, request, queryset):
        """Action para atualizar estatísticas dos clientes"""
        count = 0
        for cliente in queryset:
            cliente.atualizar_estatisticas()
            count += 1
        self.message_user(request, f'Estatísticas atualizadas para {count} clientes.')
    atualizar_estatisticas.short_description = "Atualizar estatísticas"
