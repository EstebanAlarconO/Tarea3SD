use pacientes;
create table pacientes.paciente ( id UUID PRIMARY KEY, nombre text, apellido text, rut text, email text, fecha_nacimiento text );

use recetas;
create table recetas.receta ( id UUID PRIMARY KEY, id_paciente UUID, comentario text, farmacos text, doctor text );