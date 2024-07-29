// Función para el select
document.addEventListener('DOMContentLoaded', function () {
    const customSelectTriggers = document.querySelectorAll('.custom-select-trigger');
    const customOptions = document.querySelectorAll('.custom-option');
    const roleSelected = document.getElementById('role-selected');

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
            roleSelected.value = value;

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
