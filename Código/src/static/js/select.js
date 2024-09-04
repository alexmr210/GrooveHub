// Pantalla de carga
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".add-btn.link-btn");
    buttons.forEach(function (button) {
        button.addEventListener("click", function () {
            showLoadingScreen();
        });
    });

    function showLoadingScreen() {
        const loadingScreen = document.createElement("div");
        loadingScreen.className = "loading-screen";
        const container = document.createElement("div");
        container.className = "loading-container";
        const img = document.createElement("img");
        img.src = "/static/img/loading.svg";
        img.className = "loading-image";
        const text = document.createElement("p");
        text.textContent = "Buscando";
        text.className = "loading-text";
        container.appendChild(img);
        container.appendChild(text);
        loadingScreen.appendChild(container);
        document.body.appendChild(loadingScreen);
    }
});