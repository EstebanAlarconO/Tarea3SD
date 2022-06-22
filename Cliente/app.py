from flask import Flask, render_template, request
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import tuple_factory


app = Flask(__name__)

def cassandra():
    cluster = Cluster(contact_points=['cassandra-node1', 'cassandra-node2', 'cassandra-node3'], 
                    port=9042, 
                    auth_provider=PlainTextAuthProvider(username='cassandra', password='password123'))

    session1 = cluster.connect('pacientes', wait_for_all_pools=False)
    session1.execute('USE pacientes')
    session2 = cluster.connect('recetas', wait_for_all_pools=False)
    session2.execute('USE recetas')
    return session1, session2

@app.route('/create',methods = ['GET', 'POST'])
def create_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        comentario = request.form['comentario']
        farmacos = request.form['farmacos']
        doctor = request.form['doctor']

        
        query = "SELECT rut FROM pacientes.paciente;"
        rows = pacientes.execute(query)
        lista_ruts = []
        for row in rows:
            lista_ruts.append(row.rut)
        
        if(rut not in lista_ruts):
            query = "INSERT INTO pacientes.paciente(id, nombre, apellido, rut, email, fecha_nacimiento) VALUES(now(), ?, ?, ?, ?, ?);"
            preparar = pacientes.prepare(query)
            pacientes.execute(preparar, (nombre, apellido, rut, email, fecha_nacimiento))

            query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(now(),?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (id_paciente, comentario, farmacos, doctor))
            return render_template('create.html', valores= 'Receta y usuario ingresados exitosamente')
        else:
            query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(now(),?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (id_paciente, comentario, farmacos, doctor))
            return render_template('create.html', valores= 'Receta ingresada exitosamente')

    return render_template('create.html')
@app.route('/edit',methods = ['POST'])
def edit_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        return render_template()
    return render_template()
@app.route('/delete',methods = ['POST'])
def delete_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        return render_template()
    return render_template()

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)