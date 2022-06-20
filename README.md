# Tarea3SD

<h3 align="Center"> Preguntas </h3>

1. Explique la arquitectura que Cassandra maneja. Cuando se crea el clúster ¿Cómo los nodos se conectan? ¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos? ¿Qué ocurre cuando uno de los nodos se desconecta? ¿La red generada entre los nodos siempre es eficiente? ¿Existe balanceo de carga?
    - La arquitectura de Cassandra corresponde a un sistema similar a Peer-To-Peer, en donde cada uno de sus nodos tienen la misma prioridad, además se comunican a través de Gossip. Protocolo utilizado para el intercambio de infromación de manera constante y continua. La topología corresponde a la de anillo.
    - Cuando se realiza la consulta a uno de los nodos, este actua como un coordinador en el sistema, y se encarga de dirigir la dirección de la petición recibida. Una vez realizada la petición, se genera escribe en un "Commit Log", además se escribe en un "Memtable" (escritura en memoria) y también en la "SSTable" (escritura en disco).
    - Cassandra al trabajar con replicación dentro de su arquitectura, en caso de la caída o perdida de un nodo el sistema se encuentra capacitado para seguir respondiendo ante las distintas consultas que puedan ser generadas por el usuario. Cassandra es tolerante a fallos gracias a la información de sus nodos que se encuentra replicadas en los otros.
    - La red que se genera entre los nodos no siempre es eficiente, llega un punto donde se tienen una cantidad de nodos tan grande que para acceder a nodos lejanos se puede volver contraproducente y poco eficiente. 
    - Si, Cassandra implementa RandomPartitioner como balanceador de carga. Las peticiones realizadas se distribuyen de manera aleatoria (como indica su nombre), utiliza un hash para guardar en las columnas.