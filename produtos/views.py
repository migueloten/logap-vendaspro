from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import Produto
from .serializers import ProdutoSerializer, ProdutoSelectSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet apenas para leitura de produtos (gerenciamento feito no admin)
    """
    queryset = Produto.objects.filter(ativo=True)
    serializer_class = ProdutoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'select':
            return ProdutoSelectSerializer
        return ProdutoSerializer
    
    @action(detail=False, methods=['get'])
    def select(self, request):
        """Endpoint para select de produtos"""
        produtos = self.get_queryset()
        serializer = ProdutoSelectSerializer(produtos, many=True)
        return Response(serializer.data)
