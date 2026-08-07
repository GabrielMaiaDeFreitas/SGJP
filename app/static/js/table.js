function ajustarAlturaTabelas() {

    const tabelas = document.querySelectorAll(

        ".table-responsive"

    );

    if (tabelas.length === 0) {

        return;

    }

    tabelas.forEach(tabela => {

        const topo = tabela.getBoundingClientRect().top;

        const margemInferior = 100;

        const altura = window.innerHeight - topo - margemInferior;

        tabela.style.maxHeight = `${altura}px`;

    });

}

window.addEventListener(

    "load",

    ajustarAlturaTabelas

);

window.addEventListener(

    "resize",

    ajustarAlturaTabelas

);

function ajustarAlturaTabelas() {

    const sidebar = document.querySelector(".sidebar");

    if (!sidebar) {

        return;

    }

    const tabelas = document.querySelectorAll(

        ".table-responsive"

    );

    tabelas.forEach(tabela => {

        const topoTabela =
            tabela.getBoundingClientRect().top;

        const baseSidebar =
            sidebar.getBoundingClientRect().bottom;

        const margemInferior = 32;

        const alturaDisponivel =
            baseSidebar -
            topoTabela -
            margemInferior;

        tabela.style.maxHeight =
            `${Math.max(250, alturaDisponivel)}px`;

    });
}

window.addEventListener(

    "load",

    ajustarAlturaTabelas

);

window.addEventListener(

    "resize",

    ajustarAlturaTabelas

);