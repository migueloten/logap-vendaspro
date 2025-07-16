from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, TokenCustom

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'ativo', 'created_at')
    list_filter = ('ativo', 'is_staff', 'is_superuser', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Campos Customizados', {
            'fields': ('ativo', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

@admin.register(TokenCustom)
class TokenCustomAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'expires_at', 'revogado', 'created_at')
    list_filter = ('revogado', 'expires_at')
    search_fields = ('usuario__email',)
    readonly_fields = ('token', 'created_at')
    
    fieldsets = (
        ('Informações do Token', {
            'fields': ('usuario', 'token', 'expires_at', 'revogado')
        }),
        ('Metadados', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
