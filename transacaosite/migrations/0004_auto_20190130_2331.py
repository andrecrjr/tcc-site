# Generated by Django 2.1 on 2019-01-30 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transacaosite', '0003_auto_20190106_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='valor_item',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
