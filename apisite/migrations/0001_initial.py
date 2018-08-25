# Generated by Django 2.1 on 2018-08-25 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome_item', models.CharField(max_length=35)),
                ('valor_item', models.IntegerField()),
            ],
            options={
                'verbose_name': 'item do jogo',
                'verbose_name_plural': 'itens',
                'db_table': 'item',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_transact', models.DateTimeField(auto_now_add=True)),
                ('inventario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='apisite.Inventario')),
                ('item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pega_item', to='apisite.Item')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dono_inventario', to='apisite.Profile'),
        ),
    ]
