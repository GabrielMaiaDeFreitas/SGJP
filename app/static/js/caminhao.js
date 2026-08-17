document.addEventListener("DOMContentLoaded", function () {

    const campoPlaca = document.getElementById("placa");

    if (!campoPlaca) {
        return;
    }


    campoPlaca.addEventListener("input", function () {

        let placa = campoPlaca.value
            .toUpperCase()
            .replace(/[^A-Z0-9]/g, "");


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
            /^[A-Z]{3}[0-9]{4}$/.test(placa)
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

        if (placa.length > 8) {

            placa = placa.substring(
                0,
                8
            );

        }


        campoPlaca.value = placa;

    });

});