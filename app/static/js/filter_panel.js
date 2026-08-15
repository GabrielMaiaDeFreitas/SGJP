document.addEventListener("DOMContentLoaded", () => {

    const container = document.getElementById("filters-container");
    const template = document.getElementById("filter-template");
    const btnAdicionar = document.getElementById("btn-add-filter");
    const actions = document.getElementById("filter-actions");

    if (!container) return;

    const dados = document.getElementById("filters-data");
    const btnLimpar = document.getElementById("btn-clear-filters");

    const filtrosIniciais = dados
    ? {
        campos: JSON.parse(dados.dataset.campos),
        valores: JSON.parse(dados.dataset.valores),
        valoresMin: JSON.parse(dados.dataset.valoresMin),
        valoresMax: JSON.parse(dados.dataset.valoresMax)
    }
    : {
        campos: [],
        valores: [],
        valoresMin: [],
        valoresMax: []
    };

    inicializar();

    function inicializar() {

        restaurarFiltros();

        atualizarPainel();

        btnAdicionar.addEventListener(
            "click",
            adicionarFiltro
        );

        container.addEventListener(
            "click",
            removerFiltro
        );

        btnLimpar.addEventListener(
            "click",
            limparFiltros
        );

        container.addEventListener(
            "change",
            trocarCampo
        );

        container.addEventListener(
            "input",
            atualizarPainel
        );

        container.addEventListener(
            "change",
            atualizarPainel
        );

    }

    function restaurarFiltros() {

        if (filtrosIniciais.campos.length === 0) {
            return;
        }

        let indiceValor = 0;
        let indiceMin = 0;
        let indiceMax = 0;

        filtrosIniciais.campos.forEach((campo) => {

            const linha = adicionarFiltro();

            const selectCampo =
                linha.querySelector(".filter-field");

            selectCampo.value = campo;

            const option =
                selectCampo.options[
                    selectCampo.selectedIndex
                ];

            atualizarCampoValor(
                linha,
                option
            );

            const inputs =
                linha.querySelectorAll(
                    ".filter-value input"
                );

            const select =
                linha.querySelector(
                    ".filter-value select"
                );

            /*
            * Filtro de intervalo
            *
            * Usa os arrays separados
            * de valor mínimo e máximo.
            */

            if (inputs.length === 2) {

                inputs[0].value =
                    filtrosIniciais.valoresMin[indiceMin] || "";

                inputs[1].value =
                    filtrosIniciais.valoresMax[indiceMax] || "";

                indiceMin++;
                indiceMax++;

            }

            /*
            * Filtro simples
            *
            * Usa o próximo valor disponível
            * no array valor[].
            */

            else if (inputs.length === 1) {

                inputs[0].value =
                    filtrosIniciais.valores[indiceValor] || "";

                indiceValor++;

            }

            /*
            * Filtro select
            *
            * Também usa o próximo valor disponível
            * no array valor[].
            */

            else if (select) {

                select.value =
                    filtrosIniciais.valores[indiceValor] || "";

                indiceValor++;

            }

        });

    }

    function adicionarFiltro() {

        const clone = template.content.cloneNode(true);

        container.appendChild(clone);

        const linha = container.lastElementChild;

        atualizarPainel();

        return linha;

    }

    function removerFiltro(event) {

        if (!event.target.classList.contains("btn-remove-filter")) {
            return;
        }

        event.target.closest(".filter-row").remove();
        atualizarPainel();

        const quantidade =
            container.querySelectorAll(".filter-row").length;

        if (quantidade === 0) {
            pesquisar();
        }

    }

    function limparFiltros() {

        container.replaceChildren();

        atualizarPainel();

        pesquisar();

    }

    function atualizarCampoValor(
        linha,
        option
    ) {

        const tipo =

            option.dataset.tipo;

        const subtipo =

            option.dataset.subtipo;

        const opcoes = JSON.parse(

            option.dataset.opcoes || "[]"

        );

        if (tipo === "intervalo") {

            opcoes.subtipo =

                subtipo;

        }

        const valueContainer =

            linha.querySelector(

                ".filter-value"

            );

        valueContainer.replaceChildren(

            criarCampoValor(

                tipo,

                opcoes

            )

        );

    }

    function trocarCampo(event) {

        if (!event.target.classList.contains("filter-field")) {
            return;
        }

        const campo = event.target;

        const option =
            campo.options[campo.selectedIndex];

        const linha =
            campo.closest(".filter-row");

        atualizarCampoValor(
            linha,
            option
        );

        atualizarPainel();

    }

    function atualizarPainel() {

        const filtros =

            container.querySelectorAll(

                ".filter-row"

            );

        actions.style.display =

            filtros.length === 0

                ? "none"

                : "flex";

        let podeAdicionar =

            filtros.length === 0;

        filtros.forEach(filtro => {

            const campo =

                filtro.querySelector(

                    ".filter-field"

                );

            const intervalo =

                filtro.querySelectorAll(

                    ".filter-value input"

                );

            const select =

                filtro.querySelector(

                    ".filter-value select"

                );

            let preenchido = false;

            if (

                intervalo.length === 2

            ) {

                preenchido =

                    intervalo[0].value.trim() ||

                    intervalo[1].value.trim();

            }

            else if (select) {

                preenchido =

                    select.value.trim();

            }

            else if (

                intervalo.length === 1

            ) {

                preenchido =

                    intervalo[0].value.trim();

            }

            if (

                campo.value &&

                preenchido

            ) {

                podeAdicionar = true;

            }

            else {

                podeAdicionar = false;

            }

        });

        btnAdicionar.disabled =

            !podeAdicionar;

    }

    function pesquisar() {

        const filtros =container.querySelectorAll(".filter-row");

        if (filtros.length === 0) {

            window.location = window.location.pathname;
            return;

        }

        container.closest("form").requestSubmit();
    }

});

function criarCampoValor(
    tipo,
    opcoes = []
) {

    if (tipo === "texto") {

        const input =
            document.createElement("input");

        input.type = "text";

        input.name = "valor[]";

        input.placeholder = "Digite um valor";

        return input;

    }

    if (tipo === "data") {

        const input =
            document.createElement("input");

        input.type = "date";

        input.name = "valor[]";

        return input;

    }

    if (tipo === "numero") {

        const input =
            document.createElement("input");

        input.type = "number";

        input.name = "valor[]";

        input.min = "0";

        input.step = "0.01";

        input.placeholder = "Digite um valor";

        return input;

    }

    if (tipo === "intervalo") {

        const container =
            document.createElement("div");

        container.className =
            "filter-range";

        const subtipo =

            opcoes.subtipo || "text";

        const minimo =
            document.createElement("input");

        minimo.name = "valor_min[]";

        minimo.placeholder = "De";

        const maximo =
            document.createElement("input");

        maximo.name = "valor_max[]";

        maximo.placeholder = "Até";

        if (subtipo === "data") {

            minimo.type = "date";

            maximo.type = "date";

        }

        else if (subtipo === "numero") {

            minimo.type = "number";

            maximo.type = "number";

            minimo.step = "0.01";

            maximo.step = "0.01";

            minimo.min = "0";

            maximo.min = "0";

        }

        else {

            minimo.type = "text";

            maximo.type = "text";

        }

        container.appendChild(

            minimo

        );

        container.appendChild(

            maximo

        );

        return container;

    }

    if (tipo === "select") {

        const select =
            document.createElement("select");

        select.name = "valor[]";

        const vazio =
            document.createElement("option");

        vazio.value = "";

        vazio.textContent =
            "Selecione";

        select.appendChild(

            vazio

        );

        opcoes.forEach(opcao => {

            const option =
                document.createElement("option");

            if (

                typeof opcao === "object"

            ) {

                option.value =
                    opcao.id;

                option.textContent =
                    opcao.label;

            }

            else {

                option.value =
                    opcao;

                option.textContent =
                    opcao;

            }

            select.appendChild(

                option

            );

        });

        return select;

    }

    const input =
        document.createElement("input");

    input.type = "text";

    input.name = "valor[]";

    return input;

}

