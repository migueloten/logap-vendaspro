from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    return Response({
        'message': 'VendasPro API',
        'version': '1.0',
        'endpoints': {
            'auth': '/api/v1/auth/',
            'clientes': '/api/v1/clientes/',
            'produtos': '/api/v1/produtos/',
            'pedidos': '/api/v1/pedidos/',
            'dashboard': '/api/v1/dashboard/',
            'relatorios': '/api/v1/relatorios/',
            'desafio_vogal': '/api/v1/desafio-vogal/',
            'admin': '/admin/',
            'swagger': '/api/swagger/',
            'redoc': '/api/redoc/',
            'openapi': '/api/schema/',
        }
    })

urlpatterns = [
    path('', api_root, name='home'),  # Root first
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/auth/', include('accounts.urls')),
    path('api/v1/', include('clientes.urls')),
    path('api/v1/', include('produtos.urls')),
    path('api/v1/', include('pedidos.urls')),
    path('api/v1/', include('core.urls')),
    path('api/v1/desafio-vogal/', include('desafio_vogal.urls')),
    path('api/', api_root, name='api_root'),
    
    # Documentação da API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Servir arquivos de media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar admin
admin.site.site_header = "VendasPro Admin"
admin.site.site_title = "VendasPro"
admin.site.index_title = "Painel Administrativo"
