from .models import *

dict_campos_validados = dict()
dict_retorno = dict()
                
def validaCampos(request):
    
    return_code = 0
    msgs = ''
    dados_clientes = dict()
    dados_veiculos = []
    dict_campos_validados = dict()
    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    cpf = request.POST.get('cpf')
    carros = request.POST.getlist('carro')
    placas = request.POST.getlist('placa')
    anos = request.POST.getlist('ano')

    dados_clientes = {
        'nome': nome,
        'sobrenome': sobrenome,
        'email': email,
        'cpf': cpf
    }

    dados_veiculos = list(zip(carros,placas,anos))
    list_veiculos = list()
    dict_veiculos = dict()

    for veiculo in dados_veiculos:
        dict_veiculos.update({'modelo': veiculo[0], 'placa': veiculo[1], 'ano': veiculo[2]})
        list_veiculos.append(dict_veiculos.copy())
        dict_veiculos.clear()

    if len(nome) == 0:
        msgs = 'Nome inválido ou não preenchido!'
        return_code = 1
        dict_retorno = {'msgs': msgs,
                    'return_code': return_code,
                    'dados_clientes': dados_clientes,
                    'dados_veiculos': list_veiculos,}

        return dict_retorno


    dict_campos_validados = {
        'dados_clientes': dados_clientes,
        'dados_veiculos': list_veiculos,
        'msgs': msgs,
        'return_code': return_code
    }

    return dict_campos_validados
        


def cadastraCliente(dados_clientes, dados_veiculos):
    
    return_code = 0
    msgs = ''

    #unpacking dictionary dados_clientes
    nome_cli, sobrenome_cli, email_cli, cpf_cli = dados_clientes.values()

    cliente = Cliente.objects.filter(cpf=cpf_cli)
    
    if not cliente.exists():
    
        cliente = Cliente(  nome = nome_cli,
                            email = email_cli,
                            cpf = cpf_cli
                        )

        cliente.save()

        for veiculo in dados_veiculos:

            #unpacking dictionary veiculo
            modelo, placa, ano = veiculo.values()

            busca_placa = Veiculo.objects.filter(placa = placa)

            if busca_placa.exists():
                msgs = f'Placa de carro {placa} já consta no sistema, favor verificar!'
                return_code = 1
                dict_retorno = {'msgs': msgs,
                                'return_code': return_code,
                                'dados_clientes': dados_clientes,
                                'dados_veiculos': dados_veiculos,
                    }
            else:
                veiculo = Veiculo(
                                    cliente = cliente,
                                    carro = modelo,
                                    placa = placa,
                                    ano = ano
                                )
                veiculo.save()
        
        msgs = f'Cliente {cliente.nome} cadastrado com sucesso!'
        
        dict_retorno = {'msgs': msgs,
                        'return_code': return_code,
                        'dados_clientes': dados_clientes,
                        'dados_veiculos': dados_veiculos,
                        }
        

    else:
        msgs = 'Cliente já está cadastrado!'
        return_code = 1
        dict_retorno = {'msgs': msgs,
                    'return_code': return_code,
                    'dados_clientes': dados_clientes,
                    'dados_veiculos': dados_veiculos,
                    }
    
    return dict_retorno
    	
    



            

        
        
