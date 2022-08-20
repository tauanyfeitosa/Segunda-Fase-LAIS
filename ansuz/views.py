from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from ansuz.models import Usuario, PlanoCurso, TopicoAula
from ansuz.forms import CadastroForm, LoginForms, SubmeterNovoPlanoForm, CadastrarTopicoAulaForm


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
    form = SubmeterNovoPlanoForm(request.POST or None)
    if request.method == 'POST':
        form = SubmeterNovoPlanoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                novo_plano_curso = PlanoCurso.objects.create(prof_responsavel=request.user,
                                                             titulo=form.cleaned_data.get('titulo'),
                                                             area=form.cleaned_data.get('area'),
                                                             carga_horaria=form.cleaned_data.get('carga_horaria'),
                                                             ementa=form.cleaned_data.get('ementa'),
                                                             obj_geral=form.cleaned_data.get('obj_geral'),
                                                             avaliacao=form.cleaned_data.get('avaliacao')
                                                             )
                messages.success(request,
                                 f'Seu Plano de Curso {form.cleaned_data.get("titulo")} foi cadastrado com sucesso!')
                return redirect('home')
    planos = request.user.planos_curso.all()
    for plano in planos:
        status = plano.get_status_display()
        id_plano=plano.pk
    return render(request, 'usuarios/home.html', locals())

@login_required()
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required()
def topicoscurso(request, id_plano):
    form = CadastrarTopicoAulaForm(request.POST or None)
    if request.method == 'POST':
        form = CadastrarTopicoAulaForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                novo_topico_aula = TopicoAula.objects.create(titulo=form.cleaned_data.get('titulo'),
                                                             descricao=form.cleaned_data.get('descricao'),
                                                             plano_curso=PlanoCurso.objects.get(pk=id_plano))
                messages.success(request,
                                 f'Seu Topico de Aula {form.cleaned_data.get("titulo")} foi cadastrado com sucesso!')
                return redirect('home')
    return render(request, 'usuarios/topicoscurso.html', locals())

