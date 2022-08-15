from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from dateutil.relativedelta import relativedelta
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.utils.datetime_safe import date
from localflavor.br.forms import BRCPFField
from ansuz.models import Usuario
from ansuz.models import Titulacao

class CadastroForm(UserCreationForm):
    nome_completo = forms.CharField(max_length=255, label='Nome Completo', required=True)
    cpf = BRCPFField(max_length=14, widget=forms.TextInput(attrs={'data-mask': "000.000.000-00"}), label='CPF',
                     required=True)
    data_de_nascimento = forms.DateField(widget=forms.TextInput(attrs={'data-mask': "00/00/0000"}),
                                         label='Data de Nascimento', required=True)
    titulacao = forms.ChoiceField(choices=[(None, 'Selecione')] + list(Titulacao.CHOICES), label='Titulação',
                                  required=True)
    termos_uso = forms.BooleanField(label='Termos de Uso', widget=forms.CheckboxInput(), required=True)
    password1 = forms.CharField(label='Senha', max_length=16, min_length=8, widget= forms.PasswordInput(),
                                required=True)
    password2 = forms.CharField(label='Confirmação de Senha', max_length=16, min_length=8, widget=forms.PasswordInput(),
                                required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("nome_completo", css_class="form-group col-12"),
                Column("cpf", css_class="form-group col-12"),
                Column("data_de_nascimento", css_class="form-group col-12"),
                Column("titulacao", css_class="form-group col-12"),
                Column("password1", css_class="form-group col-12"),
                Column("password2", css_class="form-group col-12"),
                Column("termos_uso", css_class="form-group col-12"),
            ),
            Submit('submit', 'Cadastrar', css_class='btn btn-primary'))

    def clean_confirmar_senha(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError("As senhas não coincidem, verifique-as novamente. Este formulário diferencia "
                                        "letras maiúsculas e minúsculas")
        return password2

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("O CPF informado já está cadastrado.")
        return cpf

    def clean_termos_de_uso(self):
        termos_uso = self.cleaned_data.get('termos_de_uso')

        if termos_uso == False:
            raise forms.ValidationError('Não é possível realizar o cadastro, é necessário concordar com os '
                                        'Termos de Uso.')
        return termos_uso

    def clean_data_de_nascimento(self):
        data_de_nascimento = self.cleaned_data.get('data_de_nascimento')
        idade = relativedelta(date.today(), data_de_nascimento).years
        if data_de_nascimento >= date.today():
            raise forms.ValidationError("Por favor, informe uma data válida")
        return data_de_nascimento

    class Meta:
        model = Usuario
        fields = ('nome_completo','cpf','data_de_nascimento','termos_uso','titulacao','password1','password2')

class LoginForms(forms.Form):
    cpf = BRCPFField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'data-mask': "000.000.000-00"}),
                     required=True)
    password1 = forms.CharField(label='Senha', max_length=16, min_length=8, widget=forms.PasswordInput(),
                                required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("cpf", css_class="form-group col-12"),
                Column("password1", css_class="form-group col-12"),
            ),
            Submit('submit', 'Entrar no Ansuz', css_class='btn btn-primary'))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf == "":
            raise forms.ValidationError("Este campo é obrigatório. Por favor, informe o seu CPF.")
        if not Usuario.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Esse CPF não está cadastrado, verifique-o ou realize um cadastro.")
        return cpf

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        cpf = self.cleaned_data.get('cpf')
        filtro = Usuario.objects.filter(cpf=cpf).first()
        password2 = filtro.password
        if check_password(password1 , password2) == False:
            raise forms.ValidationError("A senha está incorreta!")
        if password1 == "":
            raise forms.ValidationError("Esse campo é obrigatório!")