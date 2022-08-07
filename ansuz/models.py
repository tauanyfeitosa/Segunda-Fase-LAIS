from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from localflavor.br.models import BRCPFField
from datetime import date

class GerenciadorUsuarios(BaseUserManager):
    def create_user(self, cpf, nome_completo, data_de_nascimento, password=None, **outros_campos):
        if not cpf:
            raise ValueError('Usuários devem ter um CPF válido.')

        user = self.model(
            cpf=cpf,
            nome_completo=nome_completo,
            data_de_nascimento=data_de_nascimento,
            **outros_campos
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, cpf, nome_completo, data_de_nascimento, password=None, **outros_campos):
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
            **outros_campos
        )
        user.save(using=self._db)

        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    OPCOES_DE_TITULACAO = (('1', 'Graduação'), ('2', 'Especialização'), ('3', 'Mestrado'), ('4', 'Doutorado'))
    OPCOES_TERMOS_USO = (('0', 'Não'), ('1', 'Sim'))

    cpf = BRCPFField(
        max_length=14, unique=True, verbose_name='CPF',
        help_text='Esse campo é obrigatório. Máximo de 14 caracteres no formato ___.___.___-__',
        error_messages={
            'unique': "Esse CPF já está cadastrado no sistema.",
        },
    )
    nome_completo = models.CharField(verbose_name='Nome completo', max_length=255)
    data_de_nascimento = models.DateField(verbose_name='Data de nascimento')
    titulacao = models.CharField(verbose_name='Titulação', choices=OPCOES_DE_TITULACAO, max_length=1)
    termos_uso = models.CharField(verbose_name='Termos de Uso', choices=OPCOES_TERMOS_USO, max_length=1)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome_completo', 'data_de_nascimento', 'titulacao',]

    objects = GerenciadorUsuarios()

    @property
    def idade(self):
        idade = relativedelta(date.today(), self.data_de_nascimento).years
        return idade

    def __str__(self):
        return self.nome_completo