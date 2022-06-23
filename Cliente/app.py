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
        
        #Obtención datos formulario.
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        rut = request.form['rut']
        email = request.form['email']
        fecha_nacimiento = request.form['fecha_nacimiento']
        comentario = request.form['comentario']
        farmacos = request.form['farmacos']
        doctor = request.form['doctor']

        #Obtención de pacientes ya ingresados
        query = "SELECT id, rut FROM pacientes.paciente;"
        rows = pacientes.execute(query)
        lista_ruts = []
        max_id_paciente = 0
        for row in rows:
            lista_ruts.append(row.rut)
            if(max_id_paciente < row.id):
                max_id_paciente = row.id
        

        query = "SELECT id FROM recetas.receta;"
        rows = recetas.execute(query)
        max_id_receta = 0
        for row in rows:
            if(max_id_receta < row.id):
                max_id_receta = row.id

        #Si el paciente no está, se ingresa tanto él/ella como la receta
        if(rut not in lista_ruts):
            query = "INSERT INTO pacientes.paciente(id, nombre, apellido, rut, email, fecha_nacimiento) VALUES(?, ?, ?, ?, ?, ?);"
            preparar = pacientes.prepare(query)
            pacientes.execute(preparar, (max_id_paciente+1, nombre, apellido, rut, email, fecha_nacimiento))

            '''query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id'''

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(?,?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (max_id_receta + 1, max_id_paciente + 1, comentario, farmacos, doctor))

            return render_template('create.html', valores= 'Receta y usuario ingresados exitosamente')

        #Paciente ya existente, se crea solo la receta
        else:
            query= "SELECT id FROM pacientes.paciente WHERE rut='"+rut+"' ALLOW FILTERING;"
            result = pacientes.execute(query)
            for row in result:
                id_paciente = row.id

            query = "INSERT INTO recetas.receta(id, id_paciente, comentario, farmacos, doctor) VALUES(?,?,?,?,?);"
            preparar = recetas.prepare(query)
            recetas.execute(preparar, (max_id_receta + 1, id_paciente, comentario, farmacos, doctor))

            return render_template('create.html', valores= 'Receta ingresada exitosamente')

    return render_template('create.html')
@app.route('/update',methods = ['GET', 'POST'])
def edit_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':

        for key, value in request.form.items():
            if key != 'id':
                query = "UPDATE recetas.receta SET "+key+" = '"+value+"' WHERE id = "+id_receta+";"
                recetas.execute(query)
            else:
                id_receta = value
        '''query = "UPDATE recetas.receta set WHERE ALLOW FILTERING;"
        for key, value in request.form.items():

        id_receta = request.form['id_receta']
        comentario = request.form['comentario']
        farmacos = request.form['farmacos']
        doctor = request.form['doctor']'''
        return render_template('update.html', valor = 'Receta actualizada')
    return render_template('update.html')

@app.route('/delete', methods = ['GET', 'POST'])
def delete_receta():
    pacientes, recetas = cassandra()
    if request.method == 'POST':
        id_receta = request.form['id_receta']
        query = "DELETE FROM recetas.receta WHERE id ="+id_receta+" ;"
        recetas.execute(query)
    return render_template('delete.html', valor= 'Receta eliminada exitosamente')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)