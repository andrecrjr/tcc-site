# Generated by Django 2.1 on 2018-08-25 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apisite', '0003_auto_20180825_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apisite.Profile', unique=True),
        ),
    ]
