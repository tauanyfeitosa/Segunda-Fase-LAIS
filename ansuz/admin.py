from django.contrib import admin

# Register your models here.
from ansuz.models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'cpf', 'data_de_nascimento', 'titulacao',]
    list_filter = ['titulacao',]
