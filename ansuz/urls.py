from django.urls import path
from ansuz import views

urlpatterns = [

    path('', views.pginicial, name='pginicial'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout_user, name='logout'),
    path('autenticar', views.autenticar, name='autenticar'),
    path('topicoscurso/<int:id_plano>', views.topicoscurso, name='topicoscurso'),
    path('detalhar_topico/<int:id_topico>', views.detalhar_topico, name='detalhar_topico')
]