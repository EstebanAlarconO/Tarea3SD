use pacientes;
create table pacientes.paciente ( id int PRIMARY KEY, nombre text, apellido text, rut text, email text, fecha_nacimiento text );

use recetas;
create table recetas.receta ( id int PRIMARY KEY, id_paciente int, comentario text, farmacos text, doctor text );