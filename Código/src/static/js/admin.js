let newSongIndex = 0;

        function addSong() {
            const songContainer = document.createElement('div');
            songContainer.className = 'song-container';
            songContainer.dataset.index = newSongIndex;

            const titleInput = document.createElement('input');
            titleInput.type = 'text';
            titleInput.name = `newTracklist[${newSongIndex}][songTitle]`;
            titleInput.placeholder = 'Title';

            const durationInput = document.createElement('input');
            durationInput.type = 'text';
            durationInput.name = `newTracklist[${newSongIndex}][songDuration]`;
            durationInput.placeholder = 'Duration';

            const deleteButton = document.createElement('button');
            deleteButton.type = 'button';
            deleteButton.innerText = 'Eliminar';
            deleteButton.onclick = () => {
                songContainer.remove();
                updateSongIndices();
            };

            songContainer.appendChild(titleInput);
            songContainer.appendChild(durationInput);
            songContainer.appendChild(deleteButton);

            document.getElementById('newSongs').appendChild(songContainer);

            newSongIndex++;
        }

        function updateSongIndices() {
            const songContainers = document.querySelectorAll('#newSongs .song-container');
            songContainers.forEach((container, index) => {
                container.dataset.index = index;
                container.querySelector('input[name^="newTracklist["]').name = `newTracklist[${index}][songTitle]`;
                container.querySelector('input[name^="newTracklist["][name$="[songDuration]"]').name = `newTracklist[${index}][songDuration]`;
            });
            newSongIndex = songContainers.length;
        }