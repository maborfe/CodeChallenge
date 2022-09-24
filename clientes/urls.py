from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name = 'home,'), 
    path('clientes' , views.clientes, name='clientes'),
    path('home', views.home, name = 'home'),
    path('busca_cliente', views.busca_cliente, name = 'busca_cliente'),
    path('atualiza_cliente/<int:id_cliente>', views.atualiza_cliente, name='atualiza_cliente'),
    path('excluir_carro', views.excluir_carro, name='excluir_carro'),
    ]
