# Generated by Django 4.1 on 2022-08-21 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ansuz', '0010_alter_certificado_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificado',
            name='codigo_verificador',
            field=models.CharField(max_length=15, verbose_name='Código Verificador'),
        ),
        migrations.AlterField(
            model_name='planocurso',
            name='ementa',
            field=models.TextField(max_length=700, verbose_name='Ementa do Curso'),
        ),
        migrations.AlterField(
            model_name='planocurso',
            name='obj_geral',
            field=models.TextField(max_length=500, verbose_name='Objetivo Geral'),
        ),
    ]
