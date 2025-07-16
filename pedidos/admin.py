from django.contrib import admin
from .models import Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ['valor_total']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'status', 'total', 'data_pedido']
    list_filter = ['status', 'data_pedido']
    search_fields = ['numero', 'cliente__nome']
    ordering = ['-data_pedido']
    readonly_fields = ['numero', 'total', 'data_pedido']
    inlines = [PedidoItemInline]
    
    fieldsets = (
        ('Informações do Pedido', {
            'fields': ('numero', 'cliente', 'status', 'total')
        }),
        ('Endereço de Entrega', {
            'fields': ('endereco', 'cidade', 'estado', 'cep')
        }),
        ('Metadados', {
            'fields': ('data_pedido',),
            'classes': ('collapse',)
        })
    )


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'produto', 'quantidade', 'preco_unitario', 'valor_total']
    list_filter = ['created_at']
    search_fields = ['pedido__numero', 'produto__nome']
    readonly_fields = ['valor_total', 'created_at', 'updated_at']
