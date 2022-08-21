import datetime
import io
import random
from django.http import FileResponse, JsonResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.contrib import messages, auth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from ansuz.models import Usuario, PlanoCurso, TopicoAula
from ansuz.forms import CadastroForm, LoginForms, SubmeterNovoPlanoForm, CadastrarTopicoAulaForm, VerificadorForm


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
    return render(request, 'usuarios/home.html', locals())

@login_required()
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required()
def topicoscurso(request, id_plano):
    form = CadastrarTopicoAulaForm(request.POST or None)
    if request.method == 'POST':
        try:
            form = CadastrarTopicoAulaForm(request.POST)
            if form.is_valid():
                novo_topico_aula = TopicoAula.objects.create(titulo=form.cleaned_data.get('titulo'),
                                                             descricao=form.cleaned_data.get('descricao'),
                                                             plano_curso=PlanoCurso.objects.get(pk=id_plano))
                messages.success(request,
                                 f'Seu Topico de Aula {form.cleaned_data.get("titulo")} foi cadastrado com sucesso!')
                return redirect('home')

        except Exception as e:
            messages.error(request, e)
            return redirect('home')

    return render(request, 'usuarios/topicoscurso.html', locals())

@login_required
def detalhar_topico(request, id_topico):
    topicos = request.user.planos_curso.all()
    for topico in topicos:
        topico_detalhado = TopicoAula.objects.get(pk=id_topico)
        topico_descricao = topico_detalhado.text_rendered

    return render(request, 'usuarios/detalhar_topico.html', locals())

@login_required
def gerar_certificado(request, id_plano):
    plano_certificado = PlanoCurso.objects.get(pk=id_plano)
    data_hoje = datetime.datetime.now().strftime('%d/%m/%Y às %H:%M:%S')

    def generate_codigo(n):
        base = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        codigo = ""
        while n:
            codigo += base[random.randint(1, 1000) % 62]
            n -= 1
        return codigo
    codigo_verificador = generate_codigo(15)

    def mm2p(milimetros):
        return milimetros / 0.352777

    buffer = io.BytesIO()
    cnv = canvas.Canvas(buffer, pagesize=A4)
    cnv.drawImage('ansuz/imagens/lais.jpg', mm2p(100), mm2p(20), width=mm2p(15), height=mm2p(15))
    cnv.drawImage('ansuz/imagens/assinatura.jpeg', mm2p(70), mm2p(54), width=mm2p(75), height=mm2p(25))
    cnv.drawImage('ansuz/imagens/design.png', mm2p(0), mm2p(222), width=mm2p(210), height=mm2p(75))
    cnv.drawString(mm2p(40), mm2p(249), f"Dados: {plano_certificado.prof_responsavel.nome_completo} - {plano_certificado.prof_responsavel.cpf} ") #nome e cpf do professor
    cnv.drawString(mm2p(78), mm2p(230), 'CERTIFICADO DE APROVAÇÃO')
    cnv.drawString(mm2p(30), mm2p(190), "Certificamos que, para os devidos fins, o(a) professor(a)")
    cnv.drawString(mm2p(30), mm2p(180), f"{plano_certificado.prof_responsavel.nome_completo}") #nome do professor
    cnv.drawString(mm2p(30), mm2p(170), "obteve aprovação da Plataforma Ansuz - AVASUS para a")
    cnv.drawString(mm2p(30), mm2p(160), f"ministração do curso {plano_certificado.titulo}") #titulo do curso
    cnv.drawString(mm2p(30), mm2p(150), "sob o qual consta as seguintes informações:")
    cnv.drawString(mm2p(30), mm2p(140), f"Título: {plano_certificado.titulo}") #titulo do curso
    cnv.drawString(mm2p(30), mm2p(130), f"Área Temática: {plano_certificado.area.nome} ") #area tematica
    cnv.drawString(mm2p(30), mm2p(120), f"Carga Horária: {plano_certificado.carga_horaria} horas") #carga horaria
    cnv.drawString(mm2p(30), mm2p(110), f"Data de Submissão: {plano_certificado.criado_em.strftime('%d/%m/%Y às %H:%M:%S')}") #data de criação do curso
    cnv.drawString(mm2p(30), mm2p(85), f'Data de Emissão: {data_hoje}') #data de emissão do certificado
    cnv.drawString(mm2p(78), mm2p(16), 'Comunidade ANSUZ - AVASUS')
    cnv.drawString(mm2p(78), mm2p(54), 'Maria Tauany Santos Feitosa')
    cnv.drawString(mm2p(82), mm2p(48), 'Diretoria-Geral ANSUZ')
    cnv.drawString(mm2p(10), mm2p(5), f'Código de Autenticidade: {codigo_verificador} ')
    cnv.showPage()
    cnv.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='certificado_de_curso.pdf')

def autenticar_documentos(request):
    form = VerificadorForm(request.POST or None)
    if request.method == 'POST':
        form = VerificadorForm(request.POST)
        if form.is_valid:
            return redirect('home')
    return render(request, 'usuarios/autenticar.html', locals())