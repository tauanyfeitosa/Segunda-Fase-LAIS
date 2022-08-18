# Generated by Django 4.1 on 2022-08-16 14:28

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ansuz', '0007_planocurso_prof_responsavel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planocurso',
            name='carga_horaria',
            field=models.IntegerField(default=3, validators=[django.core.validators.MaxValueValidator(350), django.core.validators.MinValueValidator(3)], verbose_name='Carga Horária'),
        ),
        migrations.AlterField(
            model_name='planocurso',
            name='obj_geral',
            field=models.TextField(max_length=300, verbose_name='Objetivo Geral'),
        ),
        migrations.CreateModel(
            name='TopicoAula',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120, verbose_name='Tópico de Aula')),
                ('descricao', models.TextField(max_length=500, verbose_name='Descriçaõ')),
                ('plano_curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topicos_aula', to='ansuz.planocurso')),
            ],
        ),
    ]
