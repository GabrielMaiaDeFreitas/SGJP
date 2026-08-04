document.addEventListener("DOMContentLoaded", () => {

    const cards =
        document.querySelectorAll(".export-card");

    const btnMarcar =
        document.getElementById("btn-marcar-todas");

    const btnLimpar =
        document.getElementById("btn-desmarcar");

    const contador =
        document.getElementById("contador-colunas");

    const btnExportar =
        document.getElementById("btn-exportar");

    const formatos =
        document.querySelectorAll(
            'input[name="formatos"]'
        );

    /* =====================================================
       CHECKBOXES DAS COLUNAS
    ===================================================== */

    cards.forEach(card => {

        const checkbox =
            card.querySelector(".export-checkbox");

        checkbox.addEventListener(
            "change",
            atualizarTudo
        );

    });

    /* =====================================================
       BOTÃO SELECIONAR TODAS
    ===================================================== */

    btnMarcar.addEventListener("click", () => {

        cards.forEach(card => {

            card.querySelector(".export-checkbox").checked = true;

        });

        atualizarTudo();

    });

    /* =====================================================
       BOTÃO LIMPAR
    ===================================================== */

    btnLimpar.addEventListener("click", () => {

        cards.forEach(card => {

            card.querySelector(".export-checkbox").checked = false;

        });

        atualizarTudo();

    });

    /* =====================================================
       FORMATOS
    ===================================================== */

    formatos.forEach(formato => {

        formato.addEventListener(
            "change",
            atualizarTudo
        );

    });

    /* =====================================================
       FUNÇÃO PRINCIPAL
    ===================================================== */

    function atualizarTudo() {

        let selecionadas = 0;

        cards.forEach(card => {

            const checkbox =
                card.querySelector(".export-checkbox");

            if (checkbox.checked) {

                card.classList.add("selected");

                selecionadas++;

            } else {

                card.classList.remove("selected");

            }

        });

        const formatosSelecionados =
            document.querySelectorAll(
                'input[name="formatos"]:checked'
            ).length;

        contador.textContent =
            `${selecionadas} de ${cards.length} selecionadas`;

        btnExportar.disabled =
            (
                selecionadas === 0 ||
                formatosSelecionados === 0
            );

    }

    atualizarTudo();

});