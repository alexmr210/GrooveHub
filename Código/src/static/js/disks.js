// Información del disco
document.addEventListener('DOMContentLoaded', () => {
    const sideMsg = document.getElementById('side-msg');
    let selectedRow = null;

    document.querySelectorAll('.info-btn').forEach((link, index) => {
        link.addEventListener('click', (event) => {
            event.preventDefault(); // Evitar la acción predeterminada del enlace
            const item = collectionData[index];

            if (selectedRow === index) {
                sideMsg.innerHTML = text;
                sideMsg.className = 'message';
                selectedRow = null;
                link.style.opacity = 1; // Restablecer la opacidad
            } else {
                sideMsg.innerHTML = '';
                sideMsg.className = 'message-selected';

                const imgContainer = document.createElement('div');
                imgContainer.className = 'img-container';
                sideMsg.appendChild(imgContainer);

                const img = document.createElement('img');
                img.src = item.imageUrl;
                img.alt = 'Carátula de ' + item.title;
                imgContainer.appendChild(img);

                const titleBox = document.createElement('div');
                titleBox.className = 'p-container';
                sideMsg.appendChild(titleBox);

                const titleElement = document.createElement('p');
                titleElement.innerText = item.title;
                titleBox.appendChild(titleElement);

                const btnGroup = document.createElement('div');
                btnGroup.className = 'btn-group';

                const buttons = [
                    { class: 'details-btn', href: `${urls.details}${item.idEdicion}` },
                    { class: 'modify-btn', href: `${urls.modify}${item.idEdicion}` },
                    {
                        class: 'delete-btn',
                        href: `${urls.delete}${item.idEdicion}`,
                        confirm: '¿Estás seguro de que deseas eliminar este disco?'
                    }
                ];

                buttons.forEach(btn => {
                    const button = document.createElement('a');
                    button.className = `link-btn ${btn.class}`;
                    button.href = btn.href;

                    // Añadir data-confirm solo al botón de eliminar
                    if (btn.confirm) {
                        button.setAttribute('data-confirm', btn.confirm);
                        button.onclick = (e) => {
                            if (!confirm(btn.confirm)) {
                                e.preventDefault(); // Evitar la acción si el usuario cancela
                            }
                        };
                    }

                    btnGroup.appendChild(button);
                });

                sideMsg.appendChild(btnGroup); // Agregar el grupo de botones al div

                selectedRow = index; // Guardar el índice de la fila seleccionada
            }
        });
    });
});

// Filtros
document.addEventListener("DOMContentLoaded", function () {
    const filterBtn = document.getElementById('filter-btn');
    const filterBox = document.getElementById('filter-box');

    filterBtn.addEventListener('click', function (event) {
        event.preventDefault(); // Previene la acción por defecto del enlace

        if (filterBox.style.display === "none" || filterBox.style.display === "") {
            filterBox.style.display = "block";
        } else {
            filterBox.style.display = "none";
        }
    });
});

// Función para el select
document.addEventListener('DOMContentLoaded', function () {
    const customSelectTriggers = document.querySelectorAll('.custom-select-trigger');
    const customOptions = document.querySelectorAll('.custom-option');
    const filterBy = document.getElementById('filter-by');

    // Seleccionar la primera opción por defecto
    const firstOption = document.querySelector('.custom-option.selected');
    const customSelectTriggerSpan = document.querySelector('.custom-select-trigger span');
    if (firstOption) {
        customSelectTriggerSpan.textContent = firstOption.textContent;
    }

    customSelectTriggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            const customSelect = this.closest('.custom-select');
            customSelect.classList.toggle('open');
        });
    });

    customOptions.forEach(option => {
        option.addEventListener('click', function () {
            const customSelect = this.closest('.custom-select');
            const customSelectTrigger = customSelect.querySelector('.custom-select-trigger span');
            const value = this.getAttribute('data-value');

            customSelect.classList.remove('open');
            customSelectTrigger.textContent = this.textContent;
            filterBy.value = value;

            // Marcar la opción seleccionada
            customOptions.forEach(opt => {
                opt.classList.remove('selected');
            });
            this.classList.add('selected');

            // Aquí puedes manejar el valor seleccionado, por ejemplo, guardarlo en un input oculto si es necesario.
        });
    });

    // Cerrar el select si se hace clic fuera de él
    document.addEventListener('click', function (e) {
        const customSelect = document.querySelector('.custom-select');
        if (!customSelect.contains(e.target)) {
            customSelect.classList.remove('open');
        }
    });
});
