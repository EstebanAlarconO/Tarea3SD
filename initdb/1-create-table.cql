use pacientes;
create table pacientes.paciente ( id int PRIMARY KEY, nombre text, apellido text, rut text, email text, fecha_nacimiento text );

use recetas;
create table recetas.recetas ( id int PRIMARY KEY, id_paciente int, comentario text, farmacos text, doctor text );