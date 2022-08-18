from dateutil.relativedelta import relativedelta
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.datetime_safe import date
from localflavor.br.models import BRCPFField

class GerenciadorUsuarios(BaseUserManager):
    def create_user(self, cpf, nome_completo, data_de_nascimento, titulacao, termos_uso, password=None,
                    **outros_campos):
        if not cpf:
            raise ValueError('Usuários devem ter um CPF válido.')

        user = self.model(
            cpf=cpf,
            nome_completo=nome_completo,
            data_de_nascimento=data_de_nascimento,
            termos_uso=termos_uso,
            titulacao=titulacao,
            **outros_campos
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, cpf, nome_completo, data_de_nascimento, titulacao, termos_uso, password=None,
                         **outros_campos):
        outros_campos.setdefault('is_superuser', True)
        outros_campos.setdefault('is_staff', True)
        outros_campos.setdefault('is_active', True)

        if outros_campos.get('is_superuser') == False:
            raise ValueError('Um Superusuário deve ter "is_superuser" definido como "True".')

        if outros_campos.get('is_staff') == False:
            raise ValueError('Um Superusuário deve ter "is_staff" definido como "True".')

        user = self.create_user(
            cpf=cpf,
            nome_completo=nome_completo,
            data_de_nascimento=data_de_nascimento,
            password=password,
            titulacao=titulacao,
            termos_uso=termos_uso,
            **outros_campos
        )
        user.save(using=self._db)

        return user

class Titulacao():
    GRADUACAO = '1'
    ESPECIALIZACAO = '2'
    MESTRADO = '3'
    DOUTORADO = '4'

    CHOICES = (
        (GRADUACAO, 'Graduação'),
        (ESPECIALIZACAO, 'Especialização'),
        (MESTRADO, 'Mestrado'),
        (DOUTORADO, 'Doutorado'),
    )


class Usuario(AbstractBaseUser, PermissionsMixin):
    cpf = BRCPFField(
        max_length=14, unique=True, verbose_name='CPF',
        help_text='Esse campo é obrigatório. Máximo de 14 caracteres no formato ___.___.___-__',
        error_messages={
            'unique': "Esse CPF já está cadastrado no sistema.",
        },
    )
    nome_completo = models.CharField(verbose_name='Nome completo', max_length=255)
    data_de_nascimento = models.DateField(verbose_name='Data de nascimento')
    titulacao = models.CharField(verbose_name='Titulação', choices=Titulacao.CHOICES, max_length=1)
    termos_uso = models.BooleanField(verbose_name='Termos de Uso')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo', 'data_de_nascimento', 'titulacao', 'termos_uso']

    objects = GerenciadorUsuarios()

    def __str__(self):
        return self.nome_completo + ' - ' + self.cpf

    class Meta:
        verbose_name = ('usuário')
        verbose_name_plural = ('usuários')

    def get_nome_completo(self):
        return self.nome_completo

    def get_cpf(self):
        return self.cpf

    def get_data_de_nascimento(self):
        return self.data_de_nascimento

    def get_idade(self):
        data_de_nascimento = self.data_de_nascimento
        idade = relativedelta(date.today(),data_de_nascimento).years
        return idade

    def get_nome(self):
        return self.nome_completo.split()[0]

    def get_sobrenome(self):
        return self.nome_completo.split()[-1]

class Avaliacao():
    PROVAS = '1'
    PROJETOS = '2'
    SEMINARIOS = '3'
    OUTROS = '4'

    CHOICES = (
        (PROVAS, 'Provas'),
        (PROJETOS, 'Projetos'),
        (SEMINARIOS, 'Seminários'),
        (OUTROS, 'Outros'),
    )

class StatusCurso():
    APROVADO = '1'
    PENDENTE_DE_APROVACAO = '2'
    RECUSADO = '3'

    CHOICES = (
        (APROVADO, 'APROVADO'),
        (PENDENTE_DE_APROVACAO, 'PENDENTE DE APROVAÇÃO'),
        (RECUSADO, 'RECUSADO')
    )


class PlanoCurso(models.Model):
    prof_responsavel = models.ForeignKey('Usuario',on_delete=models.CASCADE,related_name='planos_curso')
    titulo = models.CharField(verbose_name='Título', max_length=120)
    area = models.ForeignKey('Area', on_delete=models.CASCADE, related_name='planos_curso')
    carga_horaria = models.IntegerField(verbose_name='Carga Horária', default=3, validators=[
        MaxValueValidator(350),
        MinValueValidator(3)
    ])
    ementa = models.TextField(verbose_name='Ementa do Curso', max_length=500)
    obj_geral = models.TextField(verbose_name='Objetivo Geral', max_length=300)
    avaliacao = models.CharField(verbose_name='Tipo de Avaliação', choices=Avaliacao.CHOICES, max_length=1)
    status = models.CharField(verbose_name='Status do Curso', choices=StatusCurso.CHOICES, max_length=1,
                              default=StatusCurso.PENDENTE_DE_APROVACAO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

class Area(models.Model):
    nome = models.CharField(verbose_name='Área Temática', max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class TopicoAula(models.Model):
    titulo = models.CharField(verbose_name='Tópico de Aula', max_length=120)
    descricao = models.TextField(verbose_name='Descriçaõ', max_length=500)
    plano_curso = models.ForeignKey('PlanoCurso', on_delete=models.CASCADE, related_name='topicos_aula')

    # def limite_topicos_aula(self):
