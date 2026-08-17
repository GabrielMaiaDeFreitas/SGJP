document.addEventListener(
    "DOMContentLoaded",
    function () {

        const campoCnpj =
            document.getElementById("cnpj");


        if (!campoCnpj) {
            return;
        }


        campoCnpj.addEventListener(
            "input",
            function () {

                let valor = this.value;

                valor = valor.replace(
                    /\D/g,
                    ""
                );

                valor = valor.substring(
                    0,
                    14
                );


                if (valor.length > 2) {

                    valor =
                        valor.substring(0, 2)
                        + "."
                        + valor.substring(2);

                }


                if (valor.length > 6) {

                    valor =
                        valor.substring(0, 6)
                        + "."
                        + valor.substring(6);

                }


                if (valor.length > 10) {

                    valor =
                        valor.substring(0, 10)
                        + "/"
                        + valor.substring(10);

                }


                if (valor.length > 15) {

                    valor =
                        valor.substring(0, 15)
                        + "-"
                        + valor.substring(15);

                }


                this.value = valor;

            }
        );

    }
);