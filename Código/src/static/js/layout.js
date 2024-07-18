document.addEventListener("DOMContentLoaded", function () {

    const button = document.getElementById("navbar-search");
    if (button) {
        button.addEventListener("click", function () {
            showLoadingScreen();
        });
    };

    function showLoadingScreen() {
        const loadingScreen = document.createElement("div");
        loadingScreen.className = "loading-screen";
        const container = document.createElement("div");
        container.className = "loading-container";
        const img = document.createElement("img");
        img.src = "/static/img/loading.svg";
        img.className = "loading-image";
        // img.style.animation = "spin 1s linear infinite";
        const text = document.createElement("p");
        text.textContent = "Buscando";
        text.className = "loading-text";
        container.appendChild(img);
        container.appendChild(text);
        loadingScreen.appendChild(container);
        document.body.appendChild(loadingScreen);
    }
});