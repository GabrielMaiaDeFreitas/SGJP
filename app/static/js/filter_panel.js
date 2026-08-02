document.addEventListener("DOMContentLoaded", () => {

    const container = document.getElementById("filters-container");
    const template = document.getElementById("filter-template");
    const btnAdicionar = document.getElementById("btn-add-filter");
    const actions = document.getElementById("filter-actions");

    if (!container) return;

    inicializar();

    function inicializar() {

        atualizarPainel();

        btnAdicionar.addEventListener("click", adicionarFiltro);

        container.addEventListener("click", removerFiltro);

        container.addEventListener("change", trocarCampo);

        container.addEventListener("input", atualizarPainel);

        container.addEventListener("change", atualizarPainel);

    }

    function adicionarFiltro() {

        const clone = template.content.cloneNode(true);

        container.appendChild(clone);

        atualizarPainel();

    }

    function removerFiltro(event) {

        if (!event.target.classList.contains("btn-remove-filter")) {
            return;
        }

        event.target.closest(".filter-row").remove();

        atualizarPainel();

    }

    function trocarCampo(event) {

        if (!event.target.classList.contains("filter-field")) {
            return;
        }

        const campo = event.target;

        const option = campo.options[campo.selectedIndex];

        const tipo = option.dataset.tipo;

        const opcoes = JSON.parse(
            option.dataset.opcoes || "[]"
        );

        const valueContainer = campo
            .closest(".filter-row")
            .querySelector(".filter-value");

        valueContainer.replaceChildren(
            criarCampoValor(tipo, opcoes)
        );

        atualizarPainel();

    }

    function atualizarPainel() {

        const filtros = container.querySelectorAll(".filter-row");

        actions.style.display =
            filtros.length === 0 ? "none" : "flex";

        let podeAdicionar = filtros.length === 0;

        filtros.forEach(filtro => {

            const campo = filtro.querySelector(".filter-field");

            const valor = filtro.querySelector(
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

        btnAdicionar.disabled = !podeAdicionar;

    }

});

function criarCampoValor(tipo, opcoes = []) {

    if (tipo === "texto") {

        const input = document.createElement("input");

        input.type = "text";

        input.placeholder = "Digite um valor";

        return input;

    }

    if (tipo === "data") {

        const input = document.createElement("input");

        input.type = "date";

        return input;

    }

    if (tipo === "select") {

        const select = document.createElement("select");

        const vazio = document.createElement("option");

        vazio.value = "";

        vazio.textContent = "Selecione";

        select.appendChild(vazio);

        opcoes.forEach(opcao => {

            const option = document.createElement("option");

            option.value = opcao;

            option.textContent = opcao;

            select.appendChild(option);

        });

        return select;

    }

    const input = document.createElement("input");

    input.type = "text";

    return input;

}