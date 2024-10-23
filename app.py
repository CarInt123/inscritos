from flask import Flask, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'una_clave_secreta'


def generar_id():
    if 'inscritos' in session and len(session['inscritos']) > 0:
        return max(item['id'] for item in session['inscritos']) + 1
    else:
        return 1

@app.route("/index")
def index():
    if 'inscritos' not in session:
        session['inscritos'] = []
    return render_template('index.html')

@app.route("/registrar", methods=['POST'])
def registrar():
    fecha = request.form['fecha']
    nombre = request.form['nombre']
    apellidos = request.form['apellidos']
    turno = request.form['turno']
    seminarios = ', '.join(request.form.getlist('seminarios'))

    nuevo_inscrito = {
        'id': generar_id(),
        'fecha': fecha,
        'nombre': nombre,
        'apellidos': apellidos,
        'turno': turno,
        'seminarios': seminarios
    }


    session['inscritos'].append(nuevo_inscrito)
    session.modified = True


    return redirect(url_for('listado_inscritos'))

@app.route("/inscritos")
def listado_inscritos():
    inscritos = session.get('inscritos', [])
    return render_template('inscritos.html', inscritos=inscritos)


@app.route("/editar/<int:id>")
def editar(id):
    inscritos = session.get('inscritos', [])
    inscrito = next((item for item in inscritos if item['id'] == id), None)
    return render_template('editar.html', inscrito=inscrito)


@app.route("/actualizar/<int:id>", methods=['POST'])
def actualizar(id):
    inscritos = session.get('inscritos', [])
    for inscrito in inscritos:
        if inscrito['id'] == id:
            inscrito['fecha'] = request.form['fecha']
            inscrito['nombre'] = request.form['nombre']
            inscrito['apellidos'] = request.form['apellidos']
            inscrito['turno'] = request.form['turno']
            inscrito['seminarios'] = ', '.join(request.form.getlist('seminarios'))
            break
    session['inscritos'] = inscritos
    session.modified = True
    return redirect(url_for('listado_inscritos'))


@app.route("/eliminar/<int:id>", methods=['POST'])
def eliminar(id):
    inscritos = session.get('inscritos', [])
    session['inscritos'] = [inscrito for inscrito in inscritos if inscrito['id'] != id]
    session.modified = True
    return redirect(url_for('listado_inscritos'))

if __name__ == "__main__":
    app.run(debug=True)
