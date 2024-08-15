from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)


# Función para ejecutar la consulta SQL basada en tablas seleccionadas
def query_solutions(selected_tables):
    # Consulta base
    sql_query = "SELECT s.state, s.solutions FROM solutionsTable s"

    # Agrega los JOINs dinámicos
    join_clauses = []
    for idx, table in enumerate(selected_tables):
        alias = f"c{idx}"  # Usamos un alias diferente para cada tabla
        join_clause = f"JOIN {table} {alias} ON s.state = {alias}.state"
        join_clauses.append(join_clause)

    # Combina la consulta base con las cláusulas JOIN
    if join_clauses:
        sql_query += " " + " ".join(join_clauses)

    # Ejecuta la consulta
    conn = sqlite3.connect('oo.db')  # Cambia según tu base de datos
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        results = []

    conn.close()

    return results


# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        selected_tables = request.form.getlist('tables')
        results = query_solutions(selected_tables)

    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
