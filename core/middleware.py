"""
Middleware para desabilitar CSRF em rotas da API
"""
from django.utils.deprecation import MiddlewareMixin
from django.views.decorators.csrf import csrf_exempt


class DisableCSRFMiddleware(MiddlewareMixin):
    """
    Middleware para desabilitar CSRF token em rotas da API
    """
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Desabilitar CSRF para rotas da API
        if request.path.startswith('/api/'):
            setattr(view_func, 'csrf_exempt', True)
        return None
