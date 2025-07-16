from django.db import models

class Cliente(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contato = models.CharField(max_length=20)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    @property
    def total_pedidos(self):
        return self.pedidos.count()
    
    @property
    def valor_total_gasto(self):
        total = self.pedidos.aggregate(
            total=models.Sum('total')
        )['total'] or 0
        return total
