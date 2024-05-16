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
    const scanResult = document.getElementById("scanResult");
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    scanButton.addEventListener("click", function () {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
            .then(function (stream) {
                const videoContainer = document.createElement("div");
                videoContainer.id = "videoContainer";
                document.body.appendChild(videoContainer);
                const video = document.createElement("video");
                video.setAttribute("autoplay", true);
                video.id = "videoPreview";
                video.srcObject = stream;
                videoContainer.appendChild(video);
                const closeButton = document.createElement("button");
                closeButton.innerHTML = "X";
                closeButton.id = "closeButton";
                closeButton.style.position = "absolute";
                closeButton.style.top = "10px";
                closeButton.style.right = "10px";
                closeButton.style.zIndex = "1001";
                closeButton.style.cursor = "pointer";
                closeButton.addEventListener("click", function () {
                    stream.getTracks().forEach(track => track.stop());
                    videoContainer.remove();
                });
                videoContainer.appendChild(closeButton);
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
                Quagga.onDetected(function (result) {
                    const code = result.codeResult.code;
                    console.log("Barcode detected: " + code);
                    fetch('/insert', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken
                        },
                        body: JSON.stringify({ search: code })
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
                    Quagga.stop();
                    stream.getTracks().forEach(track => track.stop());
                    videoContainer.remove();
                });
            })
            .catch(function (err) {
                console.error("Error al acceder a la cámara:", err);
            });
    });
});
