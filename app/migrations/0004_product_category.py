# Generated by Django 4.2 on 2023-05-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_product_min_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Materiais', 'Materiais'), ('Ferramentas', 'Ferramentas'), ('Diversos', 'Diversos'), ('Selecione a Categoria', 'Selecione a Categoria')], default='Selecione a Categoria', max_length=100),
        ),
    ]