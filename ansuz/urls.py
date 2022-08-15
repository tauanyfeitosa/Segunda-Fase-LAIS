from django.urls import path
from ansuz import views

urlpatterns = [

    path('', views.pginicial, name='pagina inicial'),
    path('cadastro', views.cadastro, name='cadastro'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout_user, name = 'logout'),
    path('autenticar', views.autenticar, name= 'autenticar'),
]