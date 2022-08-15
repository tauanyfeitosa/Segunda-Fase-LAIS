from django.contrib import admin

# Register your models here.
from ansuz.models import Usuario, PlanoCurso


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'data_de_nascimento', 'titulacao',]
    list_filter = ['titulacao',]

@admin.register(PlanoCurso)
class PlanoCursoAdmin(admin.ModelAdmin):
    list_display = ['titulo','carga_horaria','area','prof_responsavel','status',]
    list_filter = ['carga_horaria','area','status',]