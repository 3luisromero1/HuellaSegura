from datetime import datetime
from pathlib import Path
import sqlite3
from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'desarrollo-local-cambiar-antes-de-publicar'
DB_PATH = Path(__file__).parent / 'huellasegura.db'
TIPOS = ('Abandono', 'Maltrato', 'Peligro')
ESTADOS = ('Pendiente', 'En revisión', 'Atendido')


def conexion():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    return db


def inicializar_bd():
    with conexion() as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS ciudadanos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                contacto TEXT
            );
            CREATE TABLE IF NOT EXISTS fundaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                correo TEXT
            );
            CREATE TABLE IF NOT EXISTS reportes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL CHECK(tipo IN ('Abandono','Maltrato','Peligro')),
                descripcion TEXT NOT NULL,
                ubicacion TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'Pendiente',
                fecha TEXT NOT NULL,
                ciudadano_id INTEGER REFERENCES ciudadanos(id)
            );
            CREATE TABLE IF NOT EXISTS asignaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reporte_id INTEGER NOT NULL REFERENCES reportes(id),
                fundacion_id INTEGER NOT NULL REFERENCES fundaciones(id),
                fecha TEXT NOT NULL
            );
        ''')


def obtener_reporte(id):
    with conexion() as db:
        reporte = db.execute('SELECT * FROM reportes WHERE id = ?', (id,)).fetchone()
    if reporte is None:
        abort(404)
    return reporte


def validar(formulario):
    tipo = formulario.get('tipo', '').strip()
    descripcion = formulario.get('descripcion', '').strip()
    ubicacion = formulario.get('ubicacion', '').strip()
    estado = formulario.get('estado', 'Pendiente').strip()
    errores = []
    if tipo not in TIPOS:
        errores.append('Selecciona un tipo válido.')
    if len(descripcion) < 10:
        errores.append('La descripción debe tener al menos 10 caracteres.')
    if not ubicacion:
        errores.append('La ubicación es obligatoria.')
    if estado not in ESTADOS:
        errores.append('Selecciona un estado válido.')
    return (tipo, descripcion, ubicacion, estado), errores


@app.route('/')
def inicio():
    with conexion() as db:
        reportes = db.execute('SELECT * FROM reportes ORDER BY id DESC').fetchall()
    return render_template('inicio.html', reportes=reportes)


@app.route('/reportes/nuevo', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        datos, errores = validar(request.form)
        if not errores:
            with conexion() as db:
                db.execute('INSERT INTO reportes (tipo, descripcion, ubicacion, estado, fecha) VALUES (?, ?, ?, ?, ?)',
                           (*datos, datetime.now().strftime('%Y-%m-%d %H:%M')))
            flash('Reporte creado correctamente.', 'success')
            return redirect(url_for('inicio'))
        for error in errores:
            flash(error, 'error')
    return render_template('formulario.html', titulo='Nuevo reporte', reporte=request.form if request.method == 'POST' else None, tipos=TIPOS, estados=ESTADOS)


@app.route('/reportes/<int:id>')
def detalle(id):
    return render_template('detalle.html', reporte=obtener_reporte(id))


@app.route('/reportes/<int:id>/editar', methods=['GET', 'POST'])
def editar(id):
    reporte = obtener_reporte(id)
    if request.method == 'POST':
        datos, errores = validar(request.form)
        if not errores:
            with conexion() as db:
                db.execute('UPDATE reportes SET tipo=?, descripcion=?, ubicacion=?, estado=? WHERE id=?', (*datos, id))
            flash('Reporte actualizado.', 'success')
            return redirect(url_for('detalle', id=id))
        for error in errores:
            flash(error, 'error')
    return render_template('formulario.html', titulo='Editar reporte', reporte=request.form if request.method == 'POST' else reporte, tipos=TIPOS, estados=ESTADOS)


@app.route('/reportes/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    obtener_reporte(id)
    with conexion() as db:
        db.execute('DELETE FROM asignaciones WHERE reporte_id = ?', (id,))
        db.execute('DELETE FROM reportes WHERE id = ?', (id,))
    flash('Reporte eliminado.', 'success')
    return redirect(url_for('inicio'))


inicializar_bd()

if __name__ == '__main__':
    app.run(debug=True)
