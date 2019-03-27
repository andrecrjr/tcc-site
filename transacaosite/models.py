from django.db import models
from apisite.models import Inventario


class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nome_item = models.CharField(max_length=35)
    valor_item = models.DecimalField(decimal_places=2, max_digits=5)
    imagem_item = models.FileField(verbose_name='Imagem do item', upload_to='item_folder/', default='')
    utilizavel = models.BooleanField(default=True, verbose_name='Utilizavel')

    class Meta:
        db_table = 'item'
        verbose_name = 'item do jogo'
        verbose_name_plural = 'itens'

    def __str__(self):
        return "%s" % self.nome_item


class Transacao(models.Model):

    class Meta:
        db_table = 'transacao'
        verbose_name = 'transação do site'
        verbose_name_plural = 'transações do site'

    item_comprado = models.ManyToManyField(Item, related_name="item_usuario", through='ItemInfo')
    usuario_transacao = models.ForeignKey(Inventario, on_delete=models.CASCADE, related_name="transacao_inventario")
    status_boleto = models.BooleanField(verbose_name='Status do boleto', default=False)
    codigo_boleto = models.CharField(max_length=45, default=0)


    def __str__(self):
        if self.status_boleto is not False:
            return "Boleto pago, transação aceita"
        else:
            return "%s ainda não pagou" % self.usuario_transacao

'''
@receiver(post_save, sender=Transacao)
def create_notafiscal_from_transacao(sender, instance, created, **kwargs):
    if created:
        if instance['status_boleto'] is not False:
            NotaFiscal.objects.create(notafiscal=instance)
'''

class ItemInfo(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_in_inventario')
    transacao = models.ForeignKey(Transacao, on_delete=models.CASCADE, related_name='cart_to_transacao')
    quantidade = models.IntegerField(default=0)
    id_usuario = models.BigIntegerField()

