# Generated by Django 4.1 on 2022-08-15 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ansuz', '0004_alter_usuario_termos_uso'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Área Temática')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlanoCurso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=120, verbose_name='Título')),
                ('carga_horaria', models.PositiveIntegerField(verbose_name='Carga Horária')),
                ('ementa', models.TextField(max_length=500, verbose_name='Ementa do Curso')),
                ('obj_geral', models.CharField(max_length=300, verbose_name='Objetivo Geral')),
                ('avaliacao', models.CharField(choices=[('1', 'Provas'), ('2', 'Projetos'), ('3', 'Seminários'), ('4', 'Outros')], max_length=1, verbose_name='Tipo de Avaliação')),
                ('status', models.CharField(choices=[('1', 'APROVADO'), ('2', 'PENDENTE DE APROVAÇÃO'), ('3', 'RECUSADO')], max_length=1, verbose_name='Status do Curso')),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planos_curso', to='ansuz.area')),
            ],
        ),
    ]