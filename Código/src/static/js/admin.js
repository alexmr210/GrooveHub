let newSongIndex = 0;

function addSong() {
    const songIndexInput = document.getElementById("new_songs_amount");
    // Crear una nueva fila
    const row = document.createElement('tr');
    row.dataset.index = newSongIndex;

    // Crear la celda del título de la canción
    const titleCell = document.createElement('td');
    const titleInput = document.createElement('input');
    titleInput.type = 'text';
    titleInput.name = `newTracklist[${newSongIndex}][songTitle]`;
    titleInput.className = 'song-input admin';
    titleCell.appendChild(titleInput);

    // Crear la celda de la duración de la canción
    const durationCell = document.createElement('td');
    const durationInput = document.createElement('input');
    durationInput.type = 'text';
    durationInput.name = `newTracklist[${newSongIndex}][songDuration]`;
    durationInput.className = 'duration-input';
    durationCell.appendChild(durationInput);

    // Crear la celda del botón de eliminar
    const deleteCell = document.createElement('td');
    const deleteButton = document.createElement('button');
    deleteButton.className = 'delete-btn link-btn';
    deleteButton.type = 'button';
    deleteButton.onclick = () => {
        row.remove();
        updateSongIndices();
    };
    deleteCell.appendChild(deleteButton);

    // Añadir las celdas a la fila
    row.appendChild(titleCell);
    row.appendChild(durationCell);
    row.appendChild(deleteCell);

    // Añadir la fila a la tabla
    document.getElementById('new_songs').querySelector('tbody').appendChild(row);

    newSongIndex++;
    songIndexInput.value = newSongIndex;
}

function updateSongIndices() {
    const songIndexInput = document.getElementById("new_songs_amount");
    const songRows = document.querySelectorAll('#new_songs tbody tr');
    console.log(songRows);
    songRows.forEach((row, index) => {
        row.dataset.index = index;

        const inputs = row.querySelectorAll('input');
        console.log(row);
        const titleInput = inputs[0]; // Primer input es el título
        const durationInput = inputs[1]; // Segundo input es la duración

        // titleInput.style.backgroundColor = "red !important";

        titleInput.name = `newTracklist[${index}][songTitle]`;
        durationInput.name = `newTracklist[${index}][songDuration]`;
    });
    newSongIndex = songRows.length;
    songIndexInput.value = newSongIndex;
}

