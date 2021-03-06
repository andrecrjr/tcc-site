let rootRelatorio = document.querySelector('section.root-relatorio')

const month = document.querySelector("input[type=month]")

const monthValue = () =>{
    let date = new Date
    let dataFull = `${date.getFullYear()}-${date.getMonth()+1 < 9 ? `0${date.getMonth()+1}` : date.getMonth()+1}`
    month.value = dataFull
}

monthValue()

const filterRelatorio = ()=>{

    const botao = document.querySelector('.get-relatorio')
    
    botao.addEventListener("click", function(){
        let username = document.querySelector(".username").value
        if(month.value.length > 0){
            let boleto_status = document.querySelector(".boleto-check").checked
            const dados = requestTransactions(mountQueryFilter(month.value, boleto_status, username))
            dados.then((response)=>{
                return responseRelatorio(response, boleto_status, username)
            })
        }else{
            rootRelatorio.innerHTML = `<div class="warning">
                                            <span class="omg-warning"></span>
                                                <div class="warning-inside">Está faltando mês ou ano</div>
                                        </div>`
        }
    })
}

const responseRelatorio = (response, status_boleto, username) =>{
    const { data } = response

    const month = document.querySelector("input[type=month]")
    if(data.length > 0 || data === undefined){
        rootRelatorio.innerHTML = `<button class="generate_relatorio">Gerar relatorio</button>
        <p class="status-relatorio">${status_boleto ? `Boletos pagos`: `Boletos a pagar` } de ${month.value} ${username ? `do usuário ${username}`: ``} </p>`
        renderRelatorio(data, status_boleto, username)
    }else{
        rootRelatorio.innerHTML = `<div class="warning">
                                        <span class="omg-warning"></span>
                                        <div class="warning-inside">Não há relatórios no ano/mês ${username ? `ou do usuario`: ``} selecionado</div>
                                    </div>`
    }
}

const renderRelatorio = (data, status_boleto, username) =>{
    rootRelatorio.innerHTML +=  `<table class="relatorio" style="width:100%"><tbody class="tabela"></tbody></table>`
    let tabela = document.querySelector("tbody.tabela")
    tabelaGeral = document.querySelector(".relatorio")
    estrutura_head = `<thead>
                            <tr style="border: 1px solid black">
                                <td>Id</td>
                                <td>Codigo boleto</td>
                                <td>Username</td>
                                <td>Nome completo</td>
                                <td>Data do boleto gerado</td>
                                <td>Data do vencimento</td>
                                <td>Valor do boleto</td> 
                            </tr>       
                        </thead>`
    data.map((response)=>{
        estrutura = `<tr>
                        <td>${response.id}</td>
                        <td>${response.codigo_boleto}</td>
                        <td>${response.username}</td>
                        <td>${response.nome_completo}</td>
                        <td>${response.data_boleto_criado}</td>
                        <td>${response.expiration_boleto_date}</td>
                        <td>R$${parseFloat(response.valor_boleto).toFixed(2)}</td>
                    </tr>`
        tabela.innerHTML += estrutura
        
    })
    tabelaGeral.innerHTML += estrutura_head
    mountPrintRelatorio(data, status_boleto, username)
}


const mountPrintRelatorio = (data, status_boleto, username) =>{
    const botaoRelatorio = document.querySelector('.generate_relatorio')
    botaoRelatorio.addEventListener("click", ()=>{
        return tabelaRelatorio(data, status_boleto, username)
    })
}

function tabelaRelatorio(data, status_boleto, username){
    const month = document.querySelector("input[type=month]")
    let relatorioPage = window.open('', `Relatorio Collita ${month.value}`, 'height=800', 'width=900')
        let tabela = `
        <img src='http://127.0.0.1:8000/static/assets/collita-logo.png' width="100"/>
        <img src='http://127.0.0.1:8000/static/assets/TeamLogo.png' width="100"/>
        <h3>MageHut - Relatório de 
            ${status_boleto ? `Boletos pagos`: `Boletos a pagar` } - Transações ${month.value}</h3>
        ${username?`<h4>Usuário: ${username}</h4>`: ``}
        <table style="margin: 0 auto; border:1px black solid; width:100%">
                    <thead style="border: 1px solid black; font-weight:bold">
                        <tr>
                            <td>Id</td>
                            <td>Codigo boleto</td>
                            <td>Username</td>
                            <td>Nome completo</td>
                            <td>Data do boleto gerado</td>
                            <td>Data do vencimento</td>
                            <td>Valor do boleto</td> 
                        </tr>       
                    </thead>
                    <tbody>
                            ${data.map((response)=>{
                                return (`
                                    <tr>
                                        <td>${response.id}</td>
                                        <td>${response.codigo_boleto}</td>
                                        <td>${response.username}</td>
                                        <td>${response.nome_completo}</td>
                                        <td>${response.data_boleto_criado}</td>
                                        <td>${response.expiration_boleto_date}</td>
                                        <td>R$${parseFloat(response.valor_boleto).toFixed(2)}</td>
                                    </tr>
                                    `     
                                    )
                            })}
                    </tbody>
                </table>`
        tabela = tabela.replace(/,/g, "")
        relatorioPage.document.write(tabela)
        relatorioPage.print()
        relatorioPage.close()
}

const mountQueryFilter = (data, boleto_status, username) =>{
    const qtd_trans = document.querySelector(".qtd")
    const date = data.split('-')
    let params = {
        "mes": `${date[1]}`,
        "ano": `${date[0]}`,
        "qtd": parseInt(qtd_trans.value) > 0 ? `${qtd_trans.value}` : `0`,
        "status": boleto_status
    }
    username ? params.username = username : ``
    var queryString = Object.keys(params).map(key => key + '=' + params[key]).join('&');
    return queryString
}

const requestTransactions = async (query) =>{
    try{
        const result = await fetch(`${link}filter?${query}`)
        const response = await result.json()
        return response
    }catch (err){
        rootRelatorio.innerHTML = `<div class="warning">
                                            <span class="omg-warning"></span>
                                            <div class="warning-inside">Usuario inexistente</div>
                                    </div>`
    }
}


filterRelatorio()
