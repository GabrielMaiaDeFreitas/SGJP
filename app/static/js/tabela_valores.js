document.addEventListener("DOMContentLoaded", () => {

    const selectAdministradora = document.getElementById(
        "id_administradora"
    );

    if (!selectAdministradora) {

        return;

    }

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

});