document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "report-filter-form"
            );

        if (!form) {
            return;
        }

        const dataInicial =
            document.getElementById(
                "data_inicial"
            );

        const dataFinal =
            document.getElementById(
                "data_final"
            );

        form.addEventListener(
            "submit",
            (event) => {

                if (
                    !dataInicial.value ||
                    !dataFinal.value
                ) {

                    return;
                }

                if (
                    dataInicial.value >
                    dataFinal.value
                ) {

                    event.preventDefault();

                    alert(
                        "A data inicial não pode ser posterior à data final."
                    );

                    dataInicial.focus();

                }

            }
        );

    }
);