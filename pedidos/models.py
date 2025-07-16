from django.db import models
from django.core.validators import MinValueValidator
from clientes.models import Cliente
from produtos.models import Produto
from accounts.models import Usuario

class Pedido(models.Model):
    class StatusChoices(models.TextChoices):
        PENDENTE = 'Pendente', 'Pendente'
        EM_ANDAMENTO = 'Em andamento', 'Em andamento'
        FINALIZADO = 'Finalizado', 'Finalizado'
        CANCELADO = 'Cancelado', 'Cancelado'
    
    class MetodoEnvioChoices(models.TextChoices):
        CORREIOS_PAC = 'Correios - PAC', 'Correios - PAC'
        CORREIOS_SEDEX = 'Correios - SEDEX', 'Correios - SEDEX'
        TRANSPORTADORA = 'Transportadora', 'Transportadora'
        RETIRADA = 'Retirada no local', 'Retirada no local'
    
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=20, unique=True, editable=False)
    cliente = models.ForeignKey(
        Cliente, 
        on_delete=models.PROTECT,
        related_name='pedidos'
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDENTE
    )
    
    # Valores
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    frete = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    total = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    
    # Endereço de entrega
    endereco_cep = models.CharField(max_length=10)
    endereco_cidade = models.CharField(max_length=100)
    endereco_uf = models.CharField(max_length=2)
    endereco_rua = models.CharField(max_length=255)
    endereco_numero = models.CharField(max_length=20)
    endereco_complemento = models.CharField(max_length=100, blank=True)
    
    # Método de envio
    metodo_envio = models.CharField(
        max_length=50,
        choices=MetodoEnvioChoices.choices,
        default=MetodoEnvioChoices.CORREIOS_PAC
    )
    
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pedidos'
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-data_pedido']
        indexes = [
            models.Index(fields=['numero']),
            models.Index(fields=['cliente', 'status']),
            models.Index(fields=['data_pedido', 'status']),
            models.Index(fields=['total']),
        ]
    
    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Gerar número único do pedido
            ultimo_pedido = Pedido.objects.filter(
                numero__startswith='#'
            ).order_by('-numero').first()
            
            if ultimo_pedido:
                ultimo_numero = int(ultimo_pedido.numero[1:])
                self.numero = f"#{ultimo_numero + 1:05d}"
            else:
                self.numero = "#00001"
        
        # Calcular total baseado no frete se não foi definido
        if not self.total or self.total == 0:
            from decimal import Decimal
            self.total = self.subtotal + Decimal(str(self.frete))
        
        super().save(*args, **kwargs)
    
    def calcular_total(self):
        """Calcula o total baseado nos itens"""
        from decimal import Decimal
        self.subtotal = sum(item.valor_total for item in self.itens.all())
        self.total = self.subtotal + Decimal(str(self.frete))
        self.save(update_fields=['subtotal', 'total'])
    
    @property
    def endereco_completo(self):
        """Retorna endereço completo formatado"""
        endereco = f"{self.endereco_rua}, {self.endereco_numero}"
        if self.endereco_complemento:
            endereco += f", {self.endereco_complemento}"
        endereco += f", {self.endereco_cidade}, {self.endereco_uf}, {self.endereco_cep}"
        return endereco
    
    @property
    def total_produtos_vendidos(self):
        """Retorna total de produtos vendidos neste pedido"""
        return sum(item.quantidade for item in self.itens.all())

class PedidoItem(models.Model):
    id = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE,
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.PROTECT,
        related_name='pedido_itens'
    )
    quantidade = models.IntegerField(validators=[MinValueValidator(1)])
    preco_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    valor_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'pedido_itens'
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        unique_together = [['pedido', 'produto']]
        indexes = [
            models.Index(fields=['pedido']),
            models.Index(fields=['produto']),
        ]
    
    def __str__(self):
        return f"{self.pedido.numero} - {self.produto.nome}"
    
    def save(self, *args, **kwargs):
        # Calcular valor total automaticamente
        self.valor_total = self.quantidade * self.preco_unitario
        super().save(*args, **kwargs)
        
        # Atualizar total do pedido apenas se não estamos em uma operação bulk
        if not kwargs.get('update_fields'):
            self.pedido.calcular_total()
