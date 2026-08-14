document.addEventListener(
    "DOMContentLoaded",
    function () {

        const botaoSidebar =
            document.getElementById("btn-sidebar");

        const appLayout =
            document.querySelector(".app-layout");

        if (!botaoSidebar || !appLayout) {

            return;

        }

        botaoSidebar.addEventListener(
            "click",
            function () {

                appLayout.classList.toggle(
                    "sidebar-minimizada"
                );

                if (
                    appLayout.classList.contains(
                        "sidebar-minimizada"
                    )
                ) {

                    botaoSidebar.textContent = "→";

                    botaoSidebar.title =
                        "Mostrar menu";

                }

                else {

                    botaoSidebar.textContent = "☰";

                    botaoSidebar.title =
                        "Minimizar menu";

                }

            }
        );

    }
);