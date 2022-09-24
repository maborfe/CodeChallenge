
/**/
/* ---------------------------------------------------------------------------- */
/* ############################ INCLUIR DIV CARROS ############################ */
/* ---------------------------------------------------------------------------- */
/**/
function add_carro(){

    container = document.getElementById("form-carro")

    html = " <br> <div class='row'> <div class='col-md'> <label for='carro'>Carro</label><input type='text' class='form-control' name='carro' id='carro'> </div> "
    html += " <div class='col-md'> <label For='placa'>Placa</label><input type='text' class='form-control' name='placa'> </div> "
    html += " <div class='col-md'> <label For='ano'>Ano</label><input type='number' class='form-control' name='ano'> </div> </div>"

    container.innerHTML += html


}

/**/
/* ---------------------------------------------------------------------------- */
/* ######################### ADICIONA / ATUALIZA ############################## */
/* ---------------------------------------------------------------------------- */
/**/
function change_client_form(tipo_funcao){

    adicionar_cliente = document.getElementById('adicionar-cliente')
    update_cliente = document.getElementById('update-cliente')

    if (tipo_funcao == 'add'){
        adicionar_cliente.style.display = 'block'
        update_cliente.style.display = 'none'
        document.getElementById('messageID').style.display = 'none'
    }
    else    {
        if (tipo_funcao == 'upd'){
            update_cliente.style.display = 'block'
            adicionar_cliente.style.display = 'none'
            document.getElementById('messageID').style.display = 'none'
        }
    }

} 

/**/
/* ---------------------------------------------------------------------------- */
/* ############################ BUSCAR CLIENTE ################################ */
/* ---------------------------------------------------------------------------- */
/**/
function busca_dados_cliente(){

    id_cliente = document.getElementById('lista-cliente').value
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    
    data = new FormData()
    data.append('id_cliente', id_cliente)


    if (id_cliente != 'Selecione um Cliente')
    {
                            // o fetch serve para fazer requisições no backend, e a estrutura do mesmo é a seguinte:
                            // fetch 
                            //      (
                            //          URL,
                            //          METODO,
                            //          HEADER,
                            //          BODY
                            //       )
    fetch('busca_cliente',{
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            body: data

        }).then(function(response){
            return response.json()

        }).then(function(response){

            form_upd_cliente = document.getElementById('form-upd-cliente')
            form_upd_cliente.style.display = 'block'
            
            nome = document.getElementById('upd-nome')
            nome.value = response.dados.cliente['nome']

            //sobrenome = document.getElementById('upd-sobrenome')
            //sobrenome.value = response.dados.cliente['sobrenome']

            email = document.getElementById('upd-email')
            email.value = response.dados.cliente['email']

            cpf = document.getElementById('upd-cpf')
            cpf.value = response.dados.cliente['cpf']

 
            div_carros = document.getElementById("upd-form-carro")
            div_carros.innerHTML = ""

            for(x=0; x < response.dados.carros.length; x++){

                carro = response.dados.carros[x]

                div_carros.innerHTML += `
                    <div class='row'>
                        <div class='col-md'>
                            <label for='upd-carro'>Carro</label>
                            <input type='text' class='form-control' name='upd-carro' id='upd-carro' value='` + carro['dados']['carro'] + `'>
                        </div>
                        <div class='col-md'>
                            <label for='upd-carro'>Placa</label>
                            <input type='text' class='form-control' name='upd-placa' id='upd-placa' value='` + carro['dados']['placa'] + `'>
                        </div>
                        <div class='col-md'>
                            <label for='upd-carro'>Ano</label>      
                            <input type='number' class='form-control' name='upd-ano' id='upd-ano' value='` + carro['dados']['ano'] + `'>
                        </div>
                        <div class='col-md' style='text-align:center;>
                            <label for='upd-id-carro' >Excluir</label><br>
                            <input type='text' style='margin-top:10px;width:40px; background-color:red;color:red' class=' btn btn-danger form-control' onclick='excluir_carro(this.value)' name='upd-id-carro' id='upd-id-carro' value='` + carro['id'] + `'>
                        </div>
                    </div>
                    
                <br>`;

            }

        })
        
    }
    else
    {
        form_upd_cliente = document.getElementById('form-upd-cliente')
        form_upd_cliente.style.display = 'none'
    }
}

    
    
/**/
/* ---------------------------------------------------------------------------- */
/* ############################ ATUALIZA CARRO ################################ */
/* ---------------------------------------------------------------------------- */
/**/
function atualiza_cliente(){
    
    id_cliente = document.getElementById('lista-cliente').value

    document.getElementById('formID').action += id_cliente

    document.getElementById('formID').submit()
}

/**/
/* ---------------------------------------------------------------------------- */
/* ############################ EXCLUIR CARRO ################################# */
/* ---------------------------------------------------------------------------- */
/**/
function excluir_carro(valor_id_carro){

    id_cliente = document.getElementById('lista-cliente').value
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value
    
    dados = new FormData()
    dados.append('id_carro', valor_id_carro)

    fetch('excluir_carro',{
            method: 'POST',
            headers: {
                'X-CSRFToken': csrf_token
            },
            body: dados

        }).then(function(response){
            return response.json()

        }).then(function(response){

            
            if(response.resposta == 'ok'){
                window.location.reload()
            }
        }
    )
}
