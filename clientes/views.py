import json

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from faker import Faker

from .controllers import *
from .models import *


def home(request):

    '''
    fake = Faker(locale='pt-br')

    for i in range(20):
        cliente=Cliente()
        cliente.nome = fake.name()
        cliente.email = fake.email()
        cliente.cpf = fake.cpf()
        cliente.save()

        for i in range(3):
            carro=Veiculo()
            carro.carro = fake.country()
            carro.placa = fake.license_plate()
            carro.ano = fake.year()
            carro.cliente = cliente
            carro.save()
    '''    
     
    template = 'home.html'

    return render(request, template)




def clientes(request):
    
    template = 'clientes.html'
    contexto = ''
    
    match request.method:
    
        case 'GET':

            clientes = Cliente.objects.all()
            contexto = {
                'clientes' : clientes
            }

            return render(request, template, contexto)
    
        case 'POST':

            dict_validacao = validaCampos(request)
    
            if dict_validacao['return_code'] != 0:

                messages.add_message(request, messages.WARNING, dict_validacao['msgs'])
                contexto = {
                    'dict_cliente': dict_validacao["dados_clientes"] ,
                    'list_veiculos': dict_validacao["dados_veiculos"]
                }
                return render(request, template, contexto)
                
            else:
                
                try: 
                    
                    dict_cadastro = cadastraCliente(dict_validacao['dados_clientes'], dict_validacao['dados_veiculos'])
                    
                    if dict_cadastro['return_code'] != 0:
                        messages.add_message(request, messages.ERROR, dict_cadastro['msgs'])
                    else:
                        messages.add_message(request, messages.SUCCESS, dict_cadastro['msgs'])
                
                except:
                
                    messages.add_message(request, messages.ERROR, 'Erro desconhecido!')
                    return redirect('clientes')
            
            contexto = {
                'dict_cliente': dict_validacao["dados_clientes"] ,
                'list_veiculos': dict_validacao["dados_veiculos"]
            }
            
            return render(request, template, contexto)
            

def busca_cliente(request):

    id_cliente = request.POST.get('id_cliente')

    cliente = Cliente.objects.filter(id=id_cliente)
    # na query acima poderia até utilizar o get pra ir direto no registro que eu quero, visto que estou buscando pela chave que é o ID
    # porém o serializador abaixo espera uma queryset e não um objeto, que nesse caso é do tipo Cliente

    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']

    # aqui estamos utilizando o cliente que foi retornado na pesquisa da linha 79, como é uma queryset ou seja, uma lista de objetos, 
    # e só temos um cliente, estamos setando aqui a posição zero para pegar o objeto cliente retornado que é o único da lista.
    carros = Veiculo.objects.filter(cliente = cliente[0])
    
    carros_json = json.loads(serializers.serialize('json', carros))
    
    list_carros = list()
    
    for carro in carros_json:
        list_carros.append({'id': carro['pk'], 'dados': carro['fields']})

    allData = {'cliente': cliente_json,
                'carros': list_carros}

    return JsonResponse({'dados': allData})


def atualiza_cliente(request, id_cliente):

    template = 'clientes.html'

    nome = request.POST.get('upd-nome')
    #sobrenome = request.POST.get('upd-sobrenome')
    email = request.POST.get('upd-email')
    cpf = request.POST.get('upd-cpf')

    id_carro = request.POST.getlist('upd-id-carro')
    carro = request.POST.getlist('upd-carro')
    placa = request.POST.getlist('upd-placa')
    ano = request.POST.getlist('upd-ano')

    dados_veiculos = list(zip(id_carro,carro,placa,ano))

    cliente = Cliente.objects.get(id=id_cliente)

    try:
        cliente.nome = nome
#        cliente.sobrenome = sobrenome
        cliente.email = email
        cliente.cpf = cpf
        cliente.save()

        for carro_da_lista in dados_veiculos:
            veiculo=Veiculo.objects.get(id=carro_da_lista[0])
            veiculo.carro = carro_da_lista[1]
            veiculo.placa = carro_da_lista[2]
            veiculo.ano = carro_da_lista[3]
            veiculo.save()

        messages.add_message(request, messages.SUCCESS, 'Cliente Atualizado com Sucesso!')

        return redirect('clientes')

    except:

        return HttpResponse('Erro inesperado')

def excluir_carro(request):

    id_carro = request.POST.get('id_carro')

    
    Veiculo.objects.filter(id=id_carro).delete()

    messages.add_message(request, messages.SUCCESS, 'Carro foi excluido com sucesso.')

    return JsonResponse({'resposta': 'ok'})
