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
            valores: JSON.parse(dados.dataset.valores)
        }
        : {
            campos: [],
            valores: []
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

        filtrosIniciais.campos.forEach((campo, indice) => {

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

            const valor =
                linha.querySelector(
                    ".filter-value input, .filter-value select"
                );

            if (valor) {

                valor.value =
                    filtrosIniciais.valores[indice];

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

    function atualizarCampoValor(linha, option) {

        const tipo = option.dataset.tipo;

        const opcoes = JSON.parse(
            option.dataset.opcoes || "[]"
        );

        const valueContainer =
            linha.querySelector(".filter-value");

        valueContainer.replaceChildren(
            criarCampoValor(tipo, opcoes)
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
            container.querySelectorAll(".filter-row");

        actions.style.display =
            filtros.length === 0
                ? "none"
                : "flex";

        let podeAdicionar =
            filtros.length === 0;

        filtros.forEach(filtro => {

            const campo =
                filtro.querySelector(".filter-field");

            const valor =
                filtro.querySelector(
                    ".filter-value input, .filter-value select"
                );

            if (
                campo.value &&
                valor &&
                valor.value.trim()
            ) {

                podeAdicionar = true;

            } else {

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

function criarCampoValor(tipo, opcoes = []) {

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

    if (tipo === "select") {

        const select =
            document.createElement("select");

        select.name = "valor[]";

        const vazio =
            document.createElement("option");

        vazio.value = "";
        vazio.textContent = "Selecione";

        select.appendChild(vazio);

        opcoes.forEach(opcao => {

            const option =
                document.createElement("option");

            option.value = opcao;
            option.textContent = opcao;

            select.appendChild(option);

        });

        return select;

    }

    const input =
        document.createElement("input");

    input.type = "text";
    input.name = "valor[]";

    return input;

}

