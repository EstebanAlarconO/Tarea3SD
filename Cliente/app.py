from flask import Flask
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import socket
import os

app = Flask(__name__)


def isOpen(ip, port):
   test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      test.connect((ip, int(port)))
      test.shutdown(1)
      return True
   except:
      return False

def fakeLoadBalancer():
    ips = []
    port = 9042
    for ip in os.environ.get('CASSANDRA_SEEDS').split(','):
        if isOpen(ip, port):
            ips.append(ip)
    return ips

@app.route('/',methods = ['GET'])
def cassandra():
    cluster = Cluster(fakeLoadBalancer(), port=9042, auth_provider=PlainTextAuthProvider(username='cassandra', password='password123'))
    session = cluster.connect('pacientes', wait_for_all_pools=False)
    session.execute('USE pacientes')
    result = session.execute('SELECT * FROM pacientes')
    rows = {}
    for row in result:
        rows[row.id] = row.name
    app.logger.info(rows)
    return rows

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)