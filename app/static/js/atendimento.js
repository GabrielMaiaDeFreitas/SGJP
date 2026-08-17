document.addEventListener(
    "DOMContentLoaded",
    () => {

        inicializar();

    }
);


/* =====================================================
   ELEMENTOS
===================================================== */

const elementos = {

    administradora: document.getElementById(
        "id_administradora"
    ),

    cliente: document.getElementById(
        "id_cliente"
    ),

    recebeuPagamento: document.getElementById(
        "recebeu_pagamento"
    ),

    pagamentoSeparado: document.getElementById(
        "pagamento_separado"
    ),

    campoValorPago: document.getElementById(
        "campo_valor_pago"
    ),

    valorPago: document.getElementById(
        "valor_pago"
    ),

    houvePedagio: document.getElementById(
        "houve_pedagio"
    ),

    campoPedagio: document.getElementById(
        "campo_pedagio"
    ),

    valorPedagio: document.getElementById(
        "valor_pedagio"
    ),

    cobrarPedagio: document.getElementById(
        "cobrar_pedagio"
    ),

    campoCobrarPedagio: document.getElementById(
        "campo_cobrar_pedagio"
    ),

    cobrarHoraParada: document.getElementById(
        "cobrar_hora_parada"
    ),

    quantidadeHoraParada: document.getElementById(
        "quantidade_hora_parada"
    ),

    campoHoraParada: document.getElementById(
        "campo_hora_parada"
    ),

    cobrarHoraTrabalhada: document.getElementById(
        "cobrar_hora_trabalhada"
    ),

    quantidadeHoraTrabalhada: document.getElementById(
        "quantidade_hora_trabalhada"
    ),

    campoHoraTrabalhada: document.getElementById(
        "campo_hora_trabalhada"
    ),

    usarPatins: document.getElementById(
        "usar_patins"
    ),

    campoPatins: document.getElementById(
        "campo_patins"
    ),

    quantidadePatins: document.getElementById(
        "quantidade_patins"
    ),

    valorNegociado: document.getElementById(
        "valor_negociado"
    ),

    valorTotal: document.getElementById(
        "valor_total"
    ),

    kmTotal: document.getElementById(
        "km_total"
    ),

    tipoServico: document.getElementById(
        "id_tipo_servico"
    ),

    origem: document.getElementById(
        "origem"
    ),

    destino: document.getElementById(
        "destino"
    ),

    btnCalcularDistancia: document.getElementById(
        "btn_calcular_distancia"
    ),

    placaVeiculoRebocado: document.getElementById(
        "placa_veiculo_rebocado"
    ),

    modeloVeiculoRebocado: document.getElementById(
        "modelo_veiculo_rebocado"
    )

};


/* =====================================================
   TABELA DE VALORES
===================================================== */

const tabelaValores = {

    existe: false,

    valorSaida: 0,

    kmExcedente: 0

};


/* =====================================================
   CASO DA ADMINISTRADORA SER CLIENTE PRÓPRIO
===================================================== */

let administradoraClienteProprio = false;


/* =====================================================
   INICIALIZAÇÃO
===================================================== */

function inicializar() {

    configurarAdministradora();

    configurarPagamento();

    configurarPedagio();

    configurarHoras();

    configurarValorNegociado();

    configurarCalculo();

    configurarPlacaVeiculoRebocado();

    configurarCalculoDistancia();

    configurarConfirmacaoValorZero();

    configurarValidacaoFormulario();

    if (ATENDIMENTO) {

        atualizarFormulario().then(() => {

            configurarModoEdicao();

        });

    }

    else {

        atualizarFormulario().then(() => {

            if (RESETAR_NOVO_ATENDIMENTO) {

                resetarNovoAtendimento();

            }

        });

    }

}


/* =====================================================
   MODO DE EDIÇÃO
===================================================== */

function configurarModoEdicao() {

    if (
        Number(
            elementos.valorPedagio.value
        ) > 0
    ) {

        elementos.houvePedagio.checked = true;

    }


    if (
        Number(
            elementos.quantidadeHoraParada.value
        ) > 0
    ) {

        elementos.cobrarHoraParada.checked = true;

    }


    if (
        Number(
            elementos.quantidadeHoraTrabalhada.value
        ) > 0
    ) {

        elementos.cobrarHoraTrabalhada.checked = true;

    }


    if (
        Number(
            elementos.quantidadePatins.value
        ) > 0
    ) {

        elementos.usarPatins.checked = true;

    }


    if (
        Number(
            elementos.valorPago.value
        ) > 0
    ) {

        elementos.recebeuPagamento.checked = true;

    }


    elementos.recebeuPagamento.dispatchEvent(
        new Event("change")
    );

    elementos.houvePedagio.dispatchEvent(
        new Event("change")
    );

    elementos.cobrarHoraParada.dispatchEvent(
        new Event("change")
    );

    elementos.cobrarHoraTrabalhada.dispatchEvent(
        new Event("change")
    );

    elementos.usarPatins.dispatchEvent(
        new Event("change")
    );

}


/* =====================================================
   ADMINISTRADORA
===================================================== */

function configurarAdministradora() {

    if (
        !elementos.administradora ||
        !elementos.tipoServico
    ) {

        return;

    }


    elementos.administradora.addEventListener(
        "change",
        async function () {

            await carregarClientes();

            await buscarTabelaValores();

        }
    );


    elementos.tipoServico.addEventListener(
        "change",
        buscarTabelaValores
    );


    if (
        elementos.administradora.value
    ) {

        atualizarFormulario();

    }

}


async function carregarClientes() {

    const idAdministradora =
        elementos.administradora.value;


    if (!idAdministradora) {

        preencherClientes([]);

        return;

    }


    const resposta = await fetch(

        `/atendimentos/clientes?id_administradora=${idAdministradora}`

    );


    const dados =
        await resposta.json();


    preencherClientes(
        dados
    );

}


function preencherClientes(dados) {

    if (!elementos.cliente) {

        return;

    }


    administradoraClienteProprio =
        dados.cliente_proprio === true;


    const clientes =
        dados.clientes || [];


    elementos.cliente.innerHTML =
        "";

    elementos.cliente.disabled =
        true;


    const opcaoPadrao =
        document.createElement(
            "option"
        );


    opcaoPadrao.value =
        "";

    opcaoPadrao.selected =
        true;


    if (
        !elementos.administradora.value
    ) {

        opcaoPadrao.textContent =
            "Selecione uma administradora...";

    }

    else if (
        clientes.length === 0
    ) {

        opcaoPadrao.textContent =
            "Não há clientes cadastrados para esta administradora.";

    }

    else {

        opcaoPadrao.textContent =
            "Selecione um cliente";

    }


    elementos.cliente.appendChild(
        opcaoPadrao
    );


    clientes.forEach(
        cliente => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                cliente.id;


            option.textContent =
                cliente.nome;


            elementos.cliente.appendChild(
                option
            );

        }
    );


    if (
        clientes.length > 0
    ) {

        elementos.cliente.disabled =
            false;

    }


    if (ATENDIMENTO) {

        elementos.cliente.value =
            ATENDIMENTO.fk_cliente_id_cliente;

    }

    else if (
        dados.cliente_proprio &&
        clientes.length > 0
    ) {

        elementos.cliente.value =
            clientes[0].id;

    }

}


async function atualizarFormulario() {

    await carregarClientes();

    await buscarTabelaValores();

}


async function buscarTabelaValores() {

    const administradora =
        elementos.administradora.value;


    const tipo =
        elementos.tipoServico.value;


    removerAvisoTabelaValores();


    if (
        !administradora ||
        !tipo
    ) {

        tabelaValores.existe =
            false;

        tabelaValores.valorSaida =
            0;

        tabelaValores.kmExcedente =
            0;


        calcularValores();

        return;

    }


    const resposta =
        await fetch(

            `/atendimentos/tabela-valores` +
            `?id_administradora=${administradora}` +
            `&id_tipo_servico=${tipo}`

        );


    const dados =
        await resposta.json();


    if (!dados) {

        tabelaValores.existe =
            false;

        tabelaValores.valorSaida =
            0;

        tabelaValores.kmExcedente =
            0;


        mostrarAvisoTabelaValores();

    }

    else {

        tabelaValores.existe =
            true;


        tabelaValores.valorSaida =
            dados.valor_saida !== null
                ? Number(
                    dados.valor_saida
                )
                : 0;


        tabelaValores.kmExcedente =
            dados.valor_km_excedente !== null
                ? Number(
                    dados.valor_km_excedente
                )
                : 0;


        if (
            dados.valor_zero
        ) {

            mostrarAvisoValorZero();

        }

    }


    calcularValores();

}

/* =====================================================
   PAGAMENTO
===================================================== */

function configurarPagamento() {

    if (

        !elementos.recebeuPagamento ||

        !elementos.pagamentoSeparado ||

        !elementos.campoValorPago ||

        !elementos.valorPago

    ) {

        return;

    }

    let pagamentoSeparadoAnterior =

        elementos.pagamentoSeparado.checked;

    function atualizar() {

        const recebeuPagamento =

            elementos.recebeuPagamento.checked;

        elementos.campoValorPago.classList.toggle(

            "oculto",

            !recebeuPagamento

        );

        elementos.valorPago.disabled =

            !recebeuPagamento;

        if (recebeuPagamento) {

            elementos.pagamentoSeparado.checked = true;

            elementos.pagamentoSeparado.disabled = true;

        }

        else {

            elementos.pagamentoSeparado.disabled = false;

            elementos.pagamentoSeparado.checked =

                pagamentoSeparadoAnterior;

            elementos.valorPago.value = "0.00";

        }

    }

    elementos.recebeuPagamento.addEventListener(

        "change",

        function () {

            if (

                elementos.recebeuPagamento.checked &&

                !elementos.pagamentoSeparado.disabled

            ) {

                pagamentoSeparadoAnterior =

                    elementos.pagamentoSeparado.checked;

            }

            atualizar();

        }

    );

    atualizar();

}


/* =====================================================
   VALOR NEGOCIADO
===================================================== */

function configurarValorNegociado() {

    if (

        !elementos.valorNegociado ||

        !elementos.valorTotal

    ) {

        return;

    }

    function atualizar() {

        const negociado =
            elementos.valorNegociado.checked;

        elementos.valorTotal.readOnly =
            !negociado;

        if (!negociado) {

            calcularValores();

        }

    }

    elementos.valorNegociado.addEventListener(

        "change",

        atualizar

    );

    if (!ATENDIMENTO) {

        atualizar();

    }

}


/* =====================================================
   PEDÁGIO
===================================================== */

function configurarPedagio() {

    if (

        !elementos.houvePedagio ||

        !elementos.campoPedagio ||

        !elementos.valorPedagio ||

        !elementos.campoCobrarPedagio ||

        !elementos.cobrarPedagio

    ) {

        return;

    }

    function atualizar() {

        const houve =
            elementos.houvePedagio.checked;

        elementos.campoPedagio.classList.toggle(

            "oculto",

            !houve

        );

        elementos.campoCobrarPedagio.classList.toggle(

            "oculto",

            !houve

        );

        elementos.valorPedagio.disabled =
            !houve;

        if (!houve) {

            elementos.valorPedagio.value = "0.00";

            elementos.cobrarPedagio.checked = false;

        }

        calcularValores();

    }

    elementos.houvePedagio.addEventListener(

        "change",

        atualizar

    );

    elementos.valorPedagio.addEventListener(

        "input",

        calcularValores

    );

    elementos.cobrarPedagio.addEventListener(

        "change",

        calcularValores

    );

    atualizar();

}


/* =====================================================
   HORAS / PATINS
===================================================== */

function configurarHoras() {

    configurarCampoExpandivel(

        elementos.cobrarHoraParada,

        elementos.campoHoraParada,

        elementos.quantidadeHoraParada,

        "0"

    );

    configurarCampoExpandivel(

        elementos.cobrarHoraTrabalhada,

        elementos.campoHoraTrabalhada,

        elementos.quantidadeHoraTrabalhada,

        "0"

    );

    configurarCampoExpandivel(

        elementos.usarPatins,

        elementos.campoPatins,

        elementos.quantidadePatins,

        "0"

    );

}


/* =====================================================
   CAMPOS EXPANSÍVEIS
===================================================== */

function configurarCampoExpandivel(

    checkbox,

    container,

    input,

    valorPadrao

) {

    if (

        !checkbox ||

        !container ||

        !input

    ) {

        return;

    }

    function atualizar() {

        const ativo = checkbox.checked;

        container.classList.toggle(

            "oculto",

            !ativo

        );

        input.disabled = !ativo;

        if (!ativo) {

            input.value = valorPadrao;

        }

        calcularValores();

    }

    checkbox.addEventListener(

        "change",

        atualizar

    );

    input.addEventListener(

        "input",

        calcularValores

    );

    atualizar();

}


/* =====================================================
   CÁLCULO
===================================================== */

function configurarCalculo() {

    elementos.kmTotal?.addEventListener(

        "input",

        calcularValores

    );

    calcularValores();

}


function calcularValores() {

    let total = 0;

    total += calcularValorSaida();

    total += calcularKmExcedente();

    total += calcularPedagio();

    total += calcularHoraParada();

    total += calcularHoraTrabalhada();

    total += calcularPatins();

    atualizarValor(total);

}


/* =====================================================
   REGRAS DE CÁLCULO
===================================================== */

function calcularValorSaida() {

    return tabelaValores.valorSaida;

}


function calcularKmExcedente() {

    const km = parseFloat(

        elementos.kmTotal?.value || 0

    );

    const excedente = Math.max(

        0,

        km - CONSTANTES.KM_FRANQUIA

    );

    return (

        excedente *

        tabelaValores.kmExcedente

    );

}


function calcularPedagio() {

    if (

        !elementos.cobrarPedagio?.checked

    ) {

        return 0;

    }

    return parseFloat(

        elementos.valorPedagio.value || 0

    );

}


function calcularHoraParada() {

    if (

        !elementos.cobrarHoraParada?.checked

    ) {

        return 0;

    }

    return (

        parseInt(

            elementos.quantidadeHoraParada.value || 0

        )

        *

        CONSTANTES.VALOR_HORA_PARADA

    );

}


function calcularHoraTrabalhada() {

    if (

        !elementos.cobrarHoraTrabalhada?.checked

    ) {

        return 0;

    }

    return (

        parseInt(

            elementos.quantidadeHoraTrabalhada.value || 0

        )

        *

        CONSTANTES.VALOR_HORA_TRABALHADA

    );

}


function calcularPatins() {

    if (

        !elementos.usarPatins?.checked

    ) {

        return 0;

    }

    return (

        parseInt(

            elementos.quantidadePatins.value || 0

        )

        *

        CONSTANTES.VALOR_PATINS

    );

}


/* =====================================================
   ATUALIZAÇÃO DO CAMPO VALOR
===================================================== */

function atualizarValor(total) {

    if (

        elementos.valorNegociado?.checked

    ) {

        return;

    }

    elementos.valorTotal.value =

        total.toFixed(2);

}


/* =====================================================
   DISTÂNCIA
===================================================== */

function configurarCalculoDistancia() {

    if (

        !elementos.btnCalcularDistancia

    ) {

        return;

    }

    elementos.btnCalcularDistancia.addEventListener(

        "click",

        calcularDistancia

    );

}


async function calcularDistancia() {

    const origem =

        elementos.origem.value.trim();

    const destino =

        elementos.destino.value.trim();

    if (

        !origem ||

        !destino

    ) {

        alert(

            "Informe a origem e o destino."

        );

        return;

    }

    try {

        const resposta = await fetch(

            "/atendimentos/calcular-distancia",

            {

                method: "POST",

                headers: {

                    "Content-Type":

                        "application/json"

                },

                body: JSON.stringify({

                    origem,

                    destino

                })

            }

        );

        const dados = await resposta.json();

        if (!resposta.ok) {

            throw new Error(

                dados.erro

            );

        }

        elementos.kmTotal.value =

            dados.km.toFixed(2);

        calcularValores();

    }

    catch (erro) {

        console.error(

            erro

        );

        alert(

            erro.message ||
            "Não foi possível calcular a distância."

        );

    }

}


/* =====================================================
   AVISOS DA TABELA DE VALORES
===================================================== */

function mostrarAvisoTabelaValores() {

    let aviso =
        document.getElementById(
            "aviso-tabela-valores"
        );

    if (aviso) {

        return;

    }

    aviso = document.createElement(
        "div"
    );

    aviso.id =
        "aviso-tabela-valores";

    aviso.className =
        "alert alert-warning";

    aviso.textContent =
        "Não existe uma tabela de valores configurada para esta Administradora e Tipo de Serviço. Solicite ao administrador para configurar.";

    const campoValor =
        elementos.valorTotal.closest(
            ".form-group"
        );

    campoValor.appendChild(
        aviso
    );

}


function mostrarAvisoValorZero() {

    let aviso =
        document.getElementById(
            "aviso-valor-zero"
        );

    if (aviso) {

        return;

    }

    aviso = document.createElement(
        "div"
    );

    aviso.id =
        "aviso-valor-zero";

    aviso.className =
        "alert alert-warning";

    aviso.textContent =
        "Valor configurado como 0. O valor deverá ser preenchido manualmente.";

    const campoValor =
        elementos.valorTotal.closest(
            ".form-group"
        );

    campoValor.appendChild(
        aviso
    );

}


function removerAvisoTabelaValores() {

    const avisoTabela =
        document.getElementById(
            "aviso-tabela-valores"
        );

    if (avisoTabela) {

        avisoTabela.remove();

    }

    const avisoZero =
        document.getElementById(
            "aviso-valor-zero"
        );

    if (avisoZero) {

        avisoZero.remove();

    }

}


/* =====================================================
   CONFIRMAÇÃO DE VALOR ZERO
===================================================== */

function configurarConfirmacaoValorZero() {

    const formulario =
        document.getElementById(
            "form-atendimento"
        );

    if (!formulario) {

        return;

    }

    formulario.addEventListener(
        "submit",
        function (evento) {

            if (
                tabelaValores.existe
                &&
                tabelaValores.valorSaida === 0
                &&
                tabelaValores.kmExcedente === 0
            ) {

                const confirmar = confirm(

                    "O valor está configurado como 0. " +
                    "O valor deverá ser preenchido manualmente. " +
                    "Deseja continuar?"

                );

                if (!confirmar) {

                    evento.preventDefault();

                }

            }

        }
    );

}


/* =====================================================
   VALIDAÇÃO DO FORMULÁRIO
===================================================== */

function configurarValidacaoFormulario() {

    const formulario =
        document.getElementById(
            "form-atendimento"
        );

    if (!formulario) {

        return;

    }


    const botaoSalvar =
        formulario.querySelector(
            'button[type="submit"]'
        );

    if (!botaoSalvar) {

        return;

    }


    botaoSalvar.addEventListener(
        "click",
        function (evento) {

            if (!formulario.checkValidity()) {

                evento.preventDefault();

                const campoInvalido =
                    formulario.querySelector(
                        ":invalid"
                    );

                if (campoInvalido) {

                    campoInvalido.scrollIntoView({

                        behavior: "smooth",

                        block: "center"

                    });

                    setTimeout(

                        function () {

                            campoInvalido.reportValidity();

                        },

                        300

                    );

                }

                else {

                    formulario.reportValidity();

                }

                return;

            }

        }
    );


    formulario.addEventListener(
        "submit",
        function (evento) {

            const dataAtendimento =
                document.getElementById(
                    "data_atendimento"
                );

            if (
                dataAtendimento &&
                dataAtendimento.value &&
                dataAtendimento.max &&
                dataAtendimento.value >
                    dataAtendimento.max
            ) {

                evento.preventDefault();

                dataAtendimento.setCustomValidity(
                    "Data do Atendimento: " +
                    "não pode ser uma data futura."
                );

                dataAtendimento.scrollIntoView({

                    behavior: "smooth",

                    block: "center"

                });

                setTimeout(

                    function () {

                        dataAtendimento.reportValidity();

                    },

                    300

                );

                return;

            }

        }
    );


    formulario.addEventListener(
        "input",
        function (evento) {

            evento.target.setCustomValidity("");

        }
    );


    formulario.addEventListener(
        "change",
        function (evento) {

            evento.target.setCustomValidity("");

        }
    );

}

/* =====================================================
   RESETAR NOVO ATENDIMENTO
===================================================== */

function resetarNovoAtendimento() {

    if (ATENDIMENTO) {

        return;

    }

    elementos.tipoServico.value = "";

    if (elementos.cliente) {

        if (!administradoraClienteProprio) {

            elementos.cliente.value = "";

        }

    }

    elementos.protocolo.value = "";

    elementos.motorista.value = "";

    elementos.caminhao.value = "";

    elementos.placaVeiculoRebocado.value = "";

    elementos.modeloVeiculoRebocado.value = "";

    elementos.origem.value = "";

    elementos.destino.value = "";

    elementos.valorNegociado.checked = false;

    elementos.valorTotal.value = "0.00";

    elementos.kmTotal.value = "0";

    elementos.recebeuPagamento.checked = false;

    elementos.pagamentoSeparado.checked = false;

    elementos.valorPago.value = "0.00";

    elementos.houvePedagio.checked = false;

    elementos.valorPedagio.value = "0.00";

    elementos.cobrarPedagio.checked = false;

    elementos.cobrarHoraParada.checked = false;

    elementos.quantidadeHoraParada.value = "0";

    elementos.cobrarHoraTrabalhada.checked = false;

    elementos.quantidadeHoraTrabalhada.value = "0";

    elementos.usarPatins.checked = false;

    elementos.quantidadePatins.value = "0";

    elementos.observacao.value = "";

    removerAvisoTabelaValores();

    tabelaValores.existe = false;

    tabelaValores.valorSaida = 0;

    tabelaValores.kmExcedente = 0;

    elementos.recebeuPagamento.dispatchEvent(

        new Event("change")

    );

    elementos.houvePedagio.dispatchEvent(

        new Event("change")

    );

    elementos.cobrarHoraParada.dispatchEvent(

        new Event("change")

    );

    elementos.cobrarHoraTrabalhada.dispatchEvent(

        new Event("change")

    );

    elementos.usarPatins.dispatchEvent(

        new Event("change")

    );

    elementos.valorNegociado.dispatchEvent(

        new Event("change")

    );

    elementos.pagamentoSeparado.checked = false;

    elementos.pagamentoSeparado.disabled = false;

    calcularValores();

}


console.log(
    "ATENDIMENTO.JS FOI CARREGADO"
);


/* =====================================================
   FORMATAÇÃO DA PLACA DO VEÍCULO REBOCADO
===================================================== */

function configurarPlacaVeiculoRebocado() {

    const campoPlaca =
        document.getElementById(
            "placa_veiculo_rebocado"
        );

    if (!campoPlaca) {

        return;

    }


    campoPlaca.addEventListener(
        "input",
        function () {

            let placa =
                campoPlaca.value
                    .toUpperCase()
                    .replace(
                        /[^A-Z0-9]/g,
                        ""
                    );


            /*
             * Placa antiga
             *
             * ABC1234
             *
             * transforma em:
             *
             * ABC-1234
             */

            if (
                /^[A-Z]{3}[0-9]{4}$/.test(
                    placa
                )
            ) {

                placa =
                    placa.substring(0, 3)
                    + "-"
                    + placa.substring(3);

            }


            /*
             * Limita o tamanho máximo.
             *
             * Placa antiga formatada:
             * ABC-1234 = 8 caracteres
             *
             * Mercosul:
             * ABC1D23 = 7 caracteres
             */

            if (
                placa.length > 8
            ) {

                placa =
                    placa.substring(
                        0,
                        8
                    );

            }


            campoPlaca.value =
                placa;

        }
    );

}