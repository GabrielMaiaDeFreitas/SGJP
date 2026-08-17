document.addEventListener("DOMContentLoaded", () => {

    const selectAdministradora =
        document.getElementById(
            "id_administradora"
        );


    if (selectAdministradora) {

        selectAdministradora.addEventListener(
            "change",
            () => {

                if (!selectAdministradora.value) {
                    return;
                }

                window.location =
                    "/tabelas-valores/novo?id_administradora="
                    + selectAdministradora.value;

            }
        );

    }


    const camposValor =
        document.querySelectorAll(
            ".valor-tabela"
        );


    camposValor.forEach(
        (campo) => {

            campo.addEventListener(
                "input",
                () => {

                    if (
                        campo.value !== ""
                        &&
                        Number(campo.value) < 0
                    ) {

                        campo.value = "";

                    }

                }
            );

        }
    );

});