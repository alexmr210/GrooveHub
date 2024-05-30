CREATE TABLE usuarios(
    id_usuario VARCHAR(255) PRIMARY KEY,
    contrasena VARCHAR(255), 
    nombre VARCHAR(255), 
    email VARCHAR(255)
);

CREATE TABLE artistas(
    id_artista VARCHAR(64) PRIMARY KEY, --primary key 
    artista VARCHAR(255)     
);

CREATE TABLE discos(
    id_disco VARCHAR(64) PRIMARY KEY,   --primary key    
    titulo VARCHAR(255),        
    id_artista VARCHAR(64),              --foreign key artista
    FOREIGN KEY (id_artista) REFERENCES artistas(id_artista)
);

CREATE TABLE ediciones_disco(
    id_edicion VARCHAR(64) PRIMARY KEY,     --primary key
    id_disco VARCHAR(64),                  --foreign key discos
    edicion VARCHAR(255),
    agno INT, 
    pais VARCHAR(255),                     --año de la edición
    FOREIGN KEY (id_disco) REFERENCES discos(id_disco)
);

CREATE TABLE ediciones_usuario(
    id_edicion VARCHAR(64),
    id_usuario VARCHAR(255),
    PRIMARY KEY (id_edicion, id_usuario),
    FOREIGN KEY (id_edicion) REFERENCES ediciones_disco(id_edicion),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario)

);
CREATE TABLE canciones(
    id_cancion VARCHAR(67) PRIMARY KEY,  --primary key 
    cancion VARCHAR(255),       
    duracion VARCHAR(255) 
);

CREATE TABLE artistas_canciones(
    id_artista VARCHAR(64),              --foreign key artista
    id_cancion VARCHAR(67),              --foreign key cancion
    --primary key combinación de id_artista e id_cancion
    --por tanto id_artista e id_cancion juntos unico para cada fila
    PRIMARY KEY (id_artista, id_cancion),  
    FOREIGN KEY (id_artista) REFERENCES artistas(id_artista),
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion)
);

CREATE TABLE discos_canciones(
    id_disco VARCHAR(64),                --foreign key discos
    id_cancion VARCHAR(67),              --foreign key cancion
    --primary key combinación de 'id_disco' e 'id_cancion'
    --por tanto id_disco e id_cancion juntos unico para cada fila
    PRIMARY KEY (id_disco, id_cancion),  
    FOREIGN KEY (id_disco) REFERENCES discos(id_disco),
    FOREIGN KEY (id_cancion) REFERENCES canciones(id_cancion)
);

--Para dar permisos INSERT y SELECT al usuario nuevo creado en todas las tablas 
GRANT INSERT, SELECT ON usuarios TO usuario1;
GRANT INSERT, SELECT ON artistas TO usuario1;
GRANT INSERT, SELECT ON discos TO usuario1;
GRANT INSERT, SELECT ON ediciones_disco TO usuario1;
GRANT INSERT, SELECT ON ediciones_usuario TO usuario1;
GRANT INSERT, SELECT ON canciones TO usuario1;
GRANT INSERT, SELECT ON artistas_canciones TO usuario1;
GRANT INSERT, SELECT ON discos_canciones TO usuario1;
