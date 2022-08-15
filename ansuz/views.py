from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ansuz.models import Usuario
from ansuz.forms import CadastroForm, LoginForms


def cadastro(request):
    form = CadastroForm(request.POST or None)
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            novo_usuario = Usuario.objects.create_user(cpf=form.cleaned_data.get('cpf'), nome_completo=form.cleaned_data.get('nome_completo'),
                                                        data_de_nascimento= form.cleaned_data.get('data_de_nascimento'),
                                                        password=form.cleaned_data.get('password1'), titulacao=form.cleaned_data.get('titulacao'),
                                                        termos_uso=form.cleaned_data.get('termos_uso'))
            messages.success(request, "Seu cadastro foi realizado com sucesso!")
            return redirect('login')
    return render(request, 'usuarios/cadastro.html', locals())

def login(request):
    form = LoginForms(request.POST or None)
    if request.method == 'POST':
        form = LoginForms(request.POST)
        if form.is_valid():
            user = auth.authenticate(username=form.cleaned_data.get('cpf'), password=form.cleaned_data.get('password1'))
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Bem-vindo ao Ansuz, a plataforma de Comunidade de Práticas da AVASUS!")
                return redirect('home')
    return render(request, 'usuarios/login.html', locals())

def pginicial(request):
    return render(request, 'usuarios/pginicial.html')

def autenticar(request):
    return render(request, 'usuarios/autenticar.html')

@login_required()
def home(request):
    return render(request, 'usuarios/home.html')


@login_required()
def logout_user(request):
    logout(request)
    return redirect('login')
