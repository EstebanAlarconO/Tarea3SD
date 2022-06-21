create keyspace pacientes with replication = {'class': 'SimpleStrategy', 'replication_factor': '2'};
create keyspace recetas with replication = {'class': 'SimpleStrategy', 'replication_factor': '3'};