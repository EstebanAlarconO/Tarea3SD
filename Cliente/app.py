from cassandra.cluster import Cluster
import cassandra 
from time import sleep

sleep(20)
cluster = Cluster()
session = cluster.connect()
session.execute("CREATE KEYSPACE Tarea3 WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 3};")

print(session.execute("SELECT release_version FROM system.local").one())
print(cassandra.__version__)


while True:
    i = 0