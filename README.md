# Tarea3SD
<h3 align="Center"> Apache Cassandra </h3>

_Proyecto donde se trabaja con cassandra y python_

---------------------------------------

<h3 align="Center"> Ejecución </h3>
Para iniciar la aplicación, es necesario ejecutar los siguientes comandos, sin embargo para que funcionen debemos estar en la raíz de la carpeta:

<h4> Comandos </h4>

```
$ docker-compose build --no-cache
$ docker-compose up --force-recreate
```
Una vez iniciado se deberá esperar que Cassandra realice sus configuraciones, esto puede tardar unos minutos. Al terminar dicha configuración, se puede utilizar postman o el mismo navegador para probar el funcionamiento de la aplicación. En caso de postman se debe realizar una solicitud POST desde el apartado "Body", seleccionando "form-data" a una de las siguientes direcciones:

```
http://localhost:5000/create
http://localhost:5000/update
http://localhost:5000/delete
```
<b>Nota: <b/>Para un correcto funcionamiento en la dirección "delete" se debe ingresar la key "id_receta".
    
En el caso de utilizar navegador, se deben ingresar a una de las direcciones ya mencionadas donde se podrá rellenar un formulario.

<b>Nota:</b> Se recomienda eliminar las imágenes de docker relacionadas a Cassandra, esto es con el fin de evitar imágenes ya existentes al momento de crear los contenedores.

Se puede observar la implementación completa en el siguiente link: https://youtu.be/wBBjrEtexLs
---------------------------------------

<h3 align="Center"> Preguntas </h3>

1. Explique la arquitectura que Cassandra maneja. Cuando se crea el clúster ¿Cómo los nodos se conectan? ¿Qué ocurre cuando un cliente realiza una petición a uno de los nodos? ¿Qué ocurre cuando uno de los nodos se desconecta? ¿La red generada entre los nodos siempre es eficiente? ¿Existe balanceo de carga?
    - La arquitectura de Cassandra corresponde a un sistema similar a Peer-To-Peer, en donde cada uno de sus nodos tienen la misma prioridad, además se comunican a través de Gossip. Protocolo utilizado para el intercambio de infromación de manera constante y continua. La topología corresponde a la de anillo.
    - Cuando se realiza la consulta a uno de los nodos, este actua como un coordinador en el sistema, y se encarga de dirigir la dirección de la petición recibida. Una vez realizada la petición, se genera escribe en un "Commit Log", además se escribe en un "Memtable" (escritura en memoria) y también en la "SSTable" (escritura en disco).
    - Cassandra al trabajar con replicación dentro de su arquitectura, en caso de la caída o perdida de un nodo el sistema se encuentra capacitado para seguir respondiendo ante las distintas consultas que puedan ser generadas por el usuario. Cassandra es tolerante a fallos gracias a la información de sus nodos que se encuentra replicadas en los otros.
    - La red que se genera entre los nodos no siempre es eficiente, llega un punto donde se tienen una cantidad de nodos tan grande que para acceder a nodos lejanos se puede volver contraproducente y poco eficiente. 
    - Si, Cassandra implementa RandomPartitioner como balanceador de carga. Las peticiones realizadas se distribuyen de manera aleatoria (como indica su nombre), utiliza un hash para guardar en las columnas.
2. Cassandra posee principalmente dos estrategias para mantener redundancia en la replicación de datos. ¿Cuáles son estos? ¿Cuál es la ventaja de uno sobre otro? ¿Cuál utilizaría usted para en el caso actual y por qué? Justifique apropiadamente su respuesta.
    - Cassandra posee dos métodos para guardar la redundancia entre sus nodos. El primero es "SimpleStrategy" estrategia utilizada cuando los datos están centralizados en un solo "Data Center". Por otro lador "NetworkTopologyStrategy", es utilizado si es que se planea utilizar el clúster en múltiples "Data Centers". 
    - La principal ventaja que tiene "NetworkTopologyStrategy" sobre "SimpleStrategy" es que la mencionada anteriormente, se puede realizar el almacenamiento de copias en múltiples "Data Centers".
    - Para este trabajo basta con usar "SimpleStrategy" puesto que solo se utilizara un "Data Center" el cual contiene todos los nodos solicitados. Además esta estrategia distribuye los nodos en sentido de las agujas del reloj. 
3. Teniendo en cuenta el contexto del problema ¿Usted cree que la solución propuesta es la correcta? ¿Qué ocurre cuando se quiere escalar en la solución? ¿Qué mejoras implementaría? Oriente su respuesta hacia el Sharding (la replicación/distribución de los datos) y comente una estrategia que podría seguir para ordenar los datos.
    - Para el pequeño sistema que se esta montando cumple la solución propuesta, ya que son pocas consultas las realizadas y son pocos los nodos a utilizar. Sin embargo si lo vemos como algo mayor, es probable que no funcione de manera optima.
    - Si existiera la necesidad de escalar el sistema, se tendria que tener en cuenta que un escalamiento vertical implicaria un aumento en la memoria de los nodos. Para un escalado horizontal se debe tener en cuenta que es necesario manejar más de un "Data Center", es decir seria necesario crear nuevos clústers.
    - Dentro de las mejores que se podrian implementar son las relacionadas al "Sharding", es decir, se montarian y/o crearian nuevos clústers o "Data Centers" con las mismas caracteristicas del que ya se esta utilizando. Esta estrategia operaria de la siguiente manera, dado que un paciente puede ser asociado a diferentes recetas médicas, ya sea por área médica o simplemente porque se le recetó más de una, las tablas de los shards impares serian para los pacientes, mientras qué los shards pares serian para las recetas de esos pacientes. De esa forma podemos evitar que un shard se congestione con demasiadas consultas.

---------------------------------------

<h3 align="Left">Autores</h3>

-Esteban Alarcón
-Tomás Fuentes
