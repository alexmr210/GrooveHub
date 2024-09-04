// Función para manejar tablas
document.addEventListener("DOMContentLoaded", function () {
    const addSortEventListeners = () => {
        document.querySelectorAll('.sort-menu button').forEach(button => {
            button.addEventListener('click', () => {
                const th = button.closest('th');
                const table = th.closest('table');
                const headerIndex = Array.from(th.parentNode.children).indexOf(th);
                const rows = Array.from(table.querySelectorAll('tbody tr'));

                const order = button.classList.contains('sort-asc') ? 'asc' : 'desc';
                const comparer = (a, b) => {
                    const aValue = a.children[headerIndex].textContent.trim().toLowerCase();
                    const bValue = b.children[headerIndex].textContent.trim().toLowerCase();
                    return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
                };
                rows.sort(comparer);
                rows.forEach(row => table.querySelector('tbody').appendChild(row));
            });
        });
    };
    const addFilterEventListeners = () => {
        document.querySelectorAll('.sort-menu .filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const th = btn.closest('th');
                const table = th.closest('table');
                const headerIndex = Array.from(th.parentNode.children).indexOf(th);
                const filterValue = removeAccents(th.querySelector('.filter-input').value.trim().toLowerCase());

                table.querySelectorAll('tbody tr').forEach(row => {
                    const cellValue = removeAccents(row.children[headerIndex].textContent.trim().toLowerCase());
                    row.style.display = cellValue.includes(filterValue) ? '' : 'none';
                });
            });
        });
    };

    addSortEventListeners();
    addFilterEventListeners();
});

// Función para confirmar que se desea eliminar el disco
document.addEventListener("DOMContentLoaded", function () {
    const addConfirmationDialog = () => {
        document.querySelectorAll("a[data-confirm]").forEach(link => {
            link.addEventListener("click", function (event) {
                event.preventDefault();
                const message = this.getAttribute("data-confirm");
                if (confirm(message)) {
                    window.location.href = this.href;
                } else {
                    return false;
                }
            });
        });
    };
    addConfirmationDialog();
});

//Lectura de códigos de barras
document.addEventListener("DOMContentLoaded", function () {
    const scanButton = document.getElementById("scanButton");
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;
    let scannedCodes = [];

    function initializeScanner() {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(function (stream) {
                document.getElementById('scanText').style.display = "none";
                document.getElementById('scanButton').style.display = "none";

                const camContainer = document.createElement("div");
                camContainer.id = "camContainer";
                camContainer.classList.add("cam-container");
                document.getElementById('scannerBox').appendChild(camContainer);

                const videoContainer = document.createElement("div");
                videoContainer.id = "videoContainer";
                videoContainer.classList.add("video-container");
                document.getElementById('camContainer').appendChild(videoContainer);

                const video = document.createElement("video");
                video.setAttribute("autoplay", true);
                video.id = "videoPreview";
                video.classList.add("video-preview");
                video.srcObject = stream;
                videoContainer.appendChild(video);

                const scanInfo = document.createElement("div");
                scanInfo.id = "scanInfo";
                scanInfo.classList.add("scan-info");
                camContainer.appendChild(scanInfo);

                const infoText = document.createElement("p");
                infoText.textContent = "Códigos leídos:";
                scanInfo.appendChild(infoText);

                const codeList = document.createElement("textarea");
                codeList.id = "codeList";
                codeList.classList.add("code-list");
                scanInfo.appendChild(codeList);

                codeList.addEventListener('change', function () {
                    scannedCodes = codeList.value.split('\n').filter(code => code.trim() !== '');
                });

                const searchButton = document.createElement("button");
                searchButton.id = "scan-search";
                searchButton.innerHTML = "Buscar";
                searchButton.classList.add("link-btn");
                searchButton.classList.add("scan-option-btn");
                searchButton.addEventListener("click", function () {
                    showLoadingScreen();
                    fetch('/insert', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ search: scannedCodes })
                    })
                        .then(response => {
                            if (response.ok) {
                                window.location.href = response.url;
                            } else {
                                console.error('Error al procesar la solicitud:', response.status);
                            }
                        })
                        .catch(error => {
                            console.error('Error de red:', error);
                        });
                });
                scanInfo.appendChild(searchButton);

                const cancelButton = document.createElement("button");
                cancelButton.innerHTML = "Cancelar";
                cancelButton.classList.add("link-btn");
                cancelButton.classList.add("scan-option-btn");
                cancelButton.addEventListener("click", function () {
                    scannedCodes = [];
                    codeList.value = "";
                    stream.getTracks().forEach(track => track.stop());
                    document.getElementById('scanText').style.display = "block";
                    document.getElementById('scanButton').style.display = "flex";
                    camContainer.remove();
                    Quagga.stop();
                    Quagga.offDetected(onDetected);
                });
                scanInfo.appendChild(cancelButton);

                function onDetected(result) {
                    const code = result.codeResult.code;
                    if (!scannedCodes.includes(code)) {
                        scannedCodes.push(code);
                        codeList.value = scannedCodes.join("\n");

                        // Pausar la lectura de códigos
                        isPaused = true;
                        Quagga.pause();

                        // Mostrar el mensaje flotante
                        const message = document.createElement("div");
                        message.className = "code-read-message";
                        message.textContent = "Código leído: " + code;
                        video.parentElement.appendChild(message);

                        setTimeout(() => {
                            message.classList.add("hide");
                            setTimeout(() => {
                                message.remove();
                                Quagga.start();
                            }, 500);
                        }, 1000);
                    }
                }

                Quagga.init({
                    inputStream: {
                        name: "Live",
                        type: "LiveStream",
                        target: video
                    },
                    decoder: {
                        readers: ["ean_reader"]
                    }
                }, function (err) {
                    if (err) {
                        console.error(err);
                        return;
                    }
                    console.log("QuaggaJS initialized");
                    Quagga.start();
                });

                Quagga.onDetected(onDetected);
            })
            .catch(function (err) {
                console.error("Error al acceder a la cámara:", err);
            });
    }

    scanButton.addEventListener("click", function () {
        initializeScanner();
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

// Pantalla de carga
document.addEventListener("DOMContentLoaded", function () {
    const buttons = ["manual-search", "advanced-search", "scan-search"];
    buttons.forEach(function (buttonId) {
        const button = document.getElementById(buttonId);
        if (button) {
            button.addEventListener("click", function () {
                showLoadingScreen();
            });
        }
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

// Función para eliminar acentos de una cadena
function removeAccents(str) {
    const accents = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'À': 'A', 'È': 'E', 'Ì': 'I', 'Ò': 'O', 'Ù': 'U',
        'ä': 'a', 'ë': 'e', 'ï': 'i', 'ö': 'o', 'ü': 'u',
        'Ä': 'A', 'Ë': 'E', 'Ï': 'I', 'Ö': 'O', 'Ü': 'U',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'Â': 'A', 'Ê': 'E', 'Î': 'I', 'Ô': 'O', 'Û': 'U',
        'ã': 'a', 'õ': 'o', 'ñ': 'n',
        'Ã': 'A', 'Õ': 'O', 'Ñ': 'N',
        'ç': 'c', 'Ç': 'C'
    };

    return str.split('').map(char => accents[char] || char).join('');
}

