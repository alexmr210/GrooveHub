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
                const filterValue = th.querySelector('.filter-input').value.trim().toLowerCase();

                table.querySelectorAll('tbody tr').forEach(row => {
                    const cellValue = row.children[headerIndex].textContent.trim().toLowerCase();
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
                const camContainer = document.createElement("div");
                camContainer.id = "camContainer";
                camContainer.classList.add("cam-container");
                document.body.appendChild(camContainer);

                const video = document.createElement("video");
                video.setAttribute("autoplay", true);
                video.id = "videoPreview";
                video.classList.add("video-preview");
                video.srcObject = stream;
                camContainer.appendChild(video);

                const scanInfo = document.createElement("div");
                scanInfo.id = "scanInfo";
                scanInfo.classList.add("scan-info");
                camContainer.appendChild(scanInfo);

                const infoText = document.createElement("p");
                infoText.textContent = "Códigos leídos";
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
                searchButton.classList.add("reg-btn");
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
                cancelButton.classList.add("reg-btn");
                cancelButton.addEventListener("click", function () {
                    scannedCodes = [];
                    codeList.value = "";
                    stream.getTracks().forEach(track => track.stop());
                    camContainer.remove();
                    Quagga.stop();
                    Quagga.offDetected(onDetected);
                });
                scanInfo.appendChild(cancelButton);

                // Crear la imagen de pregunta
                const questionImage = document.createElement("img");
                questionImage.src = "/static/img/question.svg";
                questionImage.classList.add("question-image");

                // Crear el cuadro de texto emergente
                const hoverText = document.createElement("div");
                hoverText.classList.add("hover-text");
                hoverText.textContent = "¿Hay algún error en la lectura? Puedes modificar manualmente los códigos escaneados o eliminar los que finalmente no quieras buscar. Cuando hayas acabado, pulsa \"Buscar\" para hacerte con tus discos.";

                // Añadir la imagen y el cuadro de texto a scanInfo
                scanInfo.appendChild(questionImage);
                scanInfo.appendChild(hoverText);

                // Mostrar el cuadro de texto al hacer hover sobre la imagen
                questionImage.addEventListener("mouseover", function () {
                    hoverText.style.display = "block";
                });
                questionImage.addEventListener("mouseout", function () {
                    hoverText.style.display = "none";
                });

                function onDetected(result) {
                    const code = result.codeResult.code;
                    if (!scannedCodes.includes(code)) {
                        scannedCodes.push(code);
                        codeList.value = scannedCodes.join("\n");
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
