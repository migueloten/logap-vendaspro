"""
Decoradores personalizados para a API
"""
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from functools import wraps


def csrf_exempt_api(view_class):
    """
    Decorador para desabilitar CSRF em todas as ações de uma ViewSet
    """
    # Métodos HTTP que precisam de CSRF exempt
    http_methods = ['post', 'put', 'patch', 'delete']
    
    for method in http_methods:
        if hasattr(view_class, method):
            setattr(view_class, method, method_decorator(csrf_exempt)(getattr(view_class, method)))
    
    return view_class


def api_csrf_exempt(view_func):
    """
    Decorador para funções de view da API
    """
    @wraps(view_func)
    @csrf_exempt
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    return wrapper
