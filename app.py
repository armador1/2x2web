from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import json
from ScrImg import st2img, generate_image_name
import os
import shutil
app = Flask(__name__)

# Ruta a la carpeta de imágenes
IMAGE_FOLDER = 'static/Images/'

import re

def clear_image_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

def new_orientation(alg, rotation):
    # Remove spaces and replace sequences in `alg`
    alg = alg.replace(" ", "")
    alg = re.sub(r'U2', 'UU', alg)
    alg = re.sub(r"U'", 'UUU', alg)
    alg = re.sub(r'F2', 'FF', alg)
    alg = re.sub(r"F'", 'FFF', alg)
    alg = re.sub(r'R2', 'RR', alg)
    alg = re.sub(r"R'", 'RRR', alg)
    alg = re.sub(r'UUUU', '', alg)
    alg = re.sub(r'FFFF', '', alg)
    alg = re.sub(r'RRRR', '', alg)
    alg = list(alg)  # Convert to list of characters

    # Remove spaces and replace sequences in `rotation`
    rotation = rotation.replace(" ", "")
    rotation = re.sub(r'x2', 'xx', rotation)
    rotation = re.sub(r"x'", 'xxx', rotation)
    rotation = re.sub(r'z2', 'zz', rotation)
    rotation = re.sub(r"z'", 'zzz', rotation)
    rotation = re.sub(r'y2', 'yy', rotation)
    rotation = re.sub(r"y'", 'yyy', rotation)
    rotation = re.sub(r'y', 'xxxzx', rotation)
    rotation = re.sub(r'x', 'xxx', rotation)
    rotation = re.sub(r'z', 'zzz', rotation)
    rotation = list(rotation)  # Convert to list of characters

    for i in range(len(alg)):
        rotation_str = ''.join(rotation)
        rotation_str = re.sub(r'xxxx', '', rotation_str)
        rotation_str = re.sub(r'zzzz', '', rotation_str)
        rotation = list(rotation_str)

        aux = []
        for j in range(len(rotation)):
            if alg[i] == 'U':
                if rotation[j] == 'x':
                    alg[i] = 'F'
                    aux.append('x')
                elif rotation[j] == 'z':
                    alg[i] = 'R'
                    aux.extend(['z', 'x', 'x', 'x'])
            elif alg[i] == 'F':
                if rotation[j] == 'z':
                    alg[i] = 'F'
                    aux.append('z')
                elif rotation[j] == 'x':
                    alg[i] = 'U'
                    aux.extend(['z', 'x'])
            elif alg[i] == 'R':
                if rotation[j] == 'x':
                    alg[i] = 'R'
                    aux.append('x')
                elif rotation[j] == 'z':
                    alg[i] = 'U'
                    aux.append('z')
        rotation = aux

    alg = ''.join(alg)

    # Replace sequences back to notation
    alg = re.sub(r'UUUU', '', alg)
    alg = re.sub(r'FFFF', '', alg)
    alg = re.sub(r'RRRR', '', alg)

    alg = re.sub(r'UUU', "U'", alg)
    alg = re.sub(r'FFF', "F'", alg)
    alg = re.sub(r'RRR', "R'", alg)

    alg = re.sub(r'UU', 'U2', alg)
    alg = re.sub(r'FF', 'F2', alg)
    alg = re.sub(r'RR', 'R2', alg)

    alg = re.sub(r'U', ' U', alg)
    alg = re.sub(r'F', ' F', alg)
    alg = re.sub(r'R', ' R', alg)

    return alg.strip()


def rotateSolution(solution):
    rotatedSolutions = []
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "x")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "x")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "x'")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "x'")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "x")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)
    solution = new_orientation(solution, "z")
    rotatedSolutions.append(solution)

    rotatedSolutions = list(set(rotatedSolutions))

    rotatedSolutionsStr = "\n".join(str(x) for x in rotatedSolutions)

    return rotatedSolutionsStr


# def query_missing_states(include_tables, exclude_tables):
#     # Generar un alias dinámico para cada tabla
#     def generate_table_aliases(tables):
#         return {table: f"t{idx + 1}" for idx, table in enumerate(tables)}
#
#     include_aliases = generate_table_aliases(include_tables)
#     exclude_aliases = generate_table_aliases(exclude_tables)
#
#     sql_query_include = "SELECT DISTINCT s.state FROM solutionsTable s"
#     join_clauses_include = [f"JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in
#                             include_aliases.items()]
#     if join_clauses_include:
#         sql_query_include += " " + " ".join(join_clauses_include)
#
#     sql_query_exclude = None
#     if exclude_aliases:
#         sql_query_exclude = "SELECT DISTINCT s.state FROM solutionsTable s"
#         join_clauses_exclude = [f"JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in
#                                 exclude_aliases.items()]
#         if join_clauses_exclude:
#             sql_query_exclude += " " + " ".join(join_clauses_exclude)
#
#     print("Include Query:", sql_query_include)
#     print("Exclude Query:", sql_query_exclude)
#
#     conn = sqlite3.connect('oo.db')
#     cursor = conn.cursor()
#
#     try:
#         # Obtener estados incluidos
#         cursor.execute(sql_query_include)
#         included_states = set(row[0] for row in cursor.fetchall())
#         print("Included States:", included_states)
#
#         excluded_states = set()
#         if sql_query_exclude:
#             # Obtener estados excluidos
#             cursor.execute(sql_query_exclude)
#             excluded_states = set(row[0] for row in cursor.fetchall())
#             print("Excluded States:", excluded_states)
#
#         # Filtrar estados que están en las tablas incluidas pero no en las excluidas
#         missing_states = included_states - excluded_states
#         print("Missing States:", missing_states)
#
#         # Obtener detalles de los estados faltantes
#         if missing_states:
#             missing_states_list = list(missing_states)
#             placeholders = ','.join('?' * len(missing_states_list))
#             sql_details_query = f"""
#                 SELECT s.state, s.solutions
#                 FROM solutionsTable s
#                 WHERE s.state IN ({placeholders})
#             """
#             print("Details Query:", sql_details_query)
#             cursor.execute(sql_details_query, missing_states_list)
#             results = cursor.fetchall()
#
#             print("Query Results:", results)
#
#             # Estructura de los resultados
#             result_data = []
#             for state, solutions_json in results:
#                 solutions = json.loads(solutions_json)
#                 image_path = f"{state}.png"  # Asume que el nombre de la imagen es el estado con extensión .png
#                 image_url = url_for('static', filename=f'images/{image_path}')
#                 result_data.append({
#                     'state': state,
#                     'solutions': solutions,
#                     'image_url': image_url
#                 })
#
#             return result_data
#
#         return []
#     except sqlite3.Error as e:
#         print(f"Error al ejecutar la consulta: {e}")
#         return []
#     finally:
#         conn.close()


# Función actualizada para manejar la paginación
def query_missing_states(include_tables, exclude_tables, page_number=1, page_size=50):
    # Generar un alias dinámico para cada tabla
    def generate_table_aliases(tables):
        return {table: f"t{idx + 1}" for idx, table in enumerate(tables)}

    include_aliases = generate_table_aliases(include_tables)
    exclude_aliases = generate_table_aliases(exclude_tables)

    sql_query_include = "SELECT DISTINCT s.state FROM solutionsTable s"
    join_clauses_include = [f"JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in include_aliases.items()]
    if join_clauses_include:
        sql_query_include += " " + " ".join(join_clauses_include)

    sql_query_exclude = None
    if exclude_aliases:
        sql_query_exclude = "SELECT DISTINCT s.state FROM solutionsTable s"
        join_clauses_exclude = [f"JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in exclude_aliases.items()]
        if join_clauses_exclude:
            sql_query_exclude += " " + " ".join(join_clauses_exclude)

    conn = sqlite3.connect('oo.db')
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query_include)
        included_states = set(row[0] for row in cursor.fetchall())

        excluded_states = set()
        if sql_query_exclude:
            cursor.execute(sql_query_exclude)
            excluded_states = set(row[0] for row in cursor.fetchall())

        missing_states = included_states - excluded_states

        clear_image_folder(IMAGE_FOLDER)

        if missing_states:
            missing_states_list = list(missing_states)
            placeholders = ','.join('?' * len(missing_states_list))
            sql_details_query = f"""
                SELECT s.state, s.solutions 
                FROM solutionsTable s
                WHERE s.state IN ({placeholders})
                LIMIT ? OFFSET ?
            """

            offset = (page_number - 1) * page_size
            cursor.execute(sql_details_query, missing_states_list + [page_size, offset])
            results = cursor.fetchall()

            result_data = []
            for state, solutions_json in results:
                solutions = json.loads(solutions_json)
                # Generar la imagen para cada estado
                image_filename = generate_image_name(state)
                image_path = os.path.join(IMAGE_FOLDER, image_filename)
                st2img(state)  # Genera y guarda la imagen
                image_url = url_for('static', filename=f'images/{image_filename}')
                result_data.append({
                    'state': state,
                    'solutions': solutions,
                    'image_url': image_url
                })

            return result_data

        return []
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    finally:
        conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        page_number = 1  # Resetear a la primera página en una nueva consulta
        include_tables = request.form.getlist('tables_include')
        exclude_tables = request.form.getlist('tables_exclude')
    else:
        page_number = int(request.args.get('page', 1))
        include_tables = request.args.getlist('tables_include')
        exclude_tables = request.args.getlist('tables_exclude')

    results_missing_states = None
    error = None

    if include_tables:
        try:
            results_missing_states = query_missing_states(include_tables, exclude_tables, page_number)
        except Exception as e:
            error = str(e)
    else:
        if request.method == 'POST':
            error = "Debe seleccionar al menos una tabla para incluir."

    return render_template('index.html',
                           results_missing_states=results_missing_states,
                           error=error,
                           page_number=page_number,
                           include_tables=include_tables,
                           exclude_tables=exclude_tables)


@app.route('/rotate_solution')
def rotate_solution():
    solution = request.args.get('solution', '')
    rotated_solution = rotateSolution(solution)
    return jsonify({'result': rotated_solution})


if __name__ == '__main__':
    app.run(debug=True)
