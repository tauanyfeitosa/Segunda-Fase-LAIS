from django.contrib import admin
from ansuz.models import Usuario, PlanoCurso, Certificado, TopicoAula


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'data_de_nascimento', 'titulacao',]
    list_filter = ['titulacao',]

@admin.register(PlanoCurso)
class PlanoCursoAdmin(admin.ModelAdmin):
    list_display = ['titulo','carga_horaria','area','prof_responsavel','status',]
    list_filter = ['carga_horaria','area','status',]

@admin.register(Certificado)
class CertificadoAdmin(admin.ModelAdmin):
    list_display = ['plano_curso','pdf','codigo_verificador','criado_em']

@admin.register(TopicoAula)
class TopicoAulaAdmin(admin.ModelAdmin):
    list_display = ['plano_curso','titulo','criado_em']
    list_filter = ['plano_curso']


