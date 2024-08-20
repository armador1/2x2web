from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import json
from ScrImg import st2img, generate_image_name, sub_st2img
import os
import re
import shutil
import _2x2Main
import ast


app = Flask(__name__)


# Ruta a la carpeta de imágenes
IMAGE_FOLDER = 'static/Images/'
SUBIMAGE_FOLDER = 'static/SubImages/'


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
    rotated_solutions = [solution]
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "x'")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "x'")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = new_orientation(solution, "z")
    rotated_solutions.append(solution)

    rotated_solutions = list(set(rotated_solutions))

    rotated_solutions_str = "\n".join(str(x) for x in rotated_solutions)

    return rotated_solutions_str



@app.route('/state/<state_id>')
def state_details(state_id):
    conn = sqlite3.connect('oo.db')
    cursor = conn.cursor()

    try:
        # Query para obtener la información del estado específico
        cursor.execute("SELECT solutions, moves FROM solutionsTable WHERE state = ?", (state_id,))
        result = cursor.fetchone()

        if result:
            solutions_json, moves = result
            solutions = json.loads(solutions_json)
            image_filename = generate_image_name(state_id)
            if not os.path.exists(SUBIMAGE_FOLDER):
                os.makedirs(SUBIMAGE_FOLDER)
            else:
                clear_image_folder(SUBIMAGE_FOLDER)
            shutil.copy('static/'+f'Images/{image_filename}', 'static/SubImages/')
            image_url = url_for('static', filename=f'SubImages/{image_filename}')
            
            return render_template('state_details.html',
                                   state=state_id,
                                   solutions=solutions,
                                   image_url=image_url,
                                   moves=moves)
        else:
            return f"Estado {state_id} no encontrado.", 404

    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500

    finally:
        conn.close()

@app.route('/update_state', methods=['POST'])
def update_state():
    state_id = request.form.get('state_id')
    rotation = request.form.get('rotation')
    csol = request.form.get('csol')
    # print(csol)
    csol2 = csol.replace('&#34;', '"')
    new_csol = csol2.replace('&#39;', "'")
    #print(new_csol)
    solutions = ast.literal_eval(new_csol)

    if not state_id or not rotation:
        return jsonify({'error': 'Missing state_id or rotation'}), 400

    try:
        # Generar nueva solución rotada
        # conn = sqlite3.connect('oo.db')
        # cursor = conn.cursor()
        # cursor.execute("SELECT solutions FROM solutionsTable WHERE state = ?", (state_id,))
        # result = cursor.fetchone()
        # if result:
        #     solutions_json = result[0]
        #     solutions = json.loads(solutions_json)
        # if not result:
        #     return jsonify({'error': 'State not found'}), 404

        # solutions_json = result[0]
        # solutions = json.loads(solutions_json)

        # Aquí se debe rotar las soluciones y generar una nueva imagen
        # La función rotateSolution() ya rota las soluciones.
        rotated_solutions = []
        if rotation == 'x3':
            rot2 = "x'"
        elif rotation == 'y3':
            rot2 = "y'"
        elif rotation == 'z3':
            rot2 = "z'"
        else:
            rot2 = rotation
        for sol in solutions:
            rotated_solutions.append(new_orientation(sol,rot2))  # Suponiendo que la solución a rotar es la primera

        rot = getattr(_2x2Main, rotation)
        # print(state_id)
        new_state_id = str(_2x2Main.s2sList(rot(_2x2Main.sList2s(ast.literal_eval(state_id)))))
        # print(new_state_id)
        clear_image_folder(SUBIMAGE_FOLDER)
        image_filename = generate_image_name(new_state_id)
        sub_st2img(new_state_id)

        new_image_url = url_for('static', filename=f'SubImages/{image_filename}')

        return jsonify({'new_image_url': new_image_url,
                        'new_state_id' : new_state_id,
                        'solutions' : rotated_solutions,
                        'str_solutions' : str(rotated_solutions)})

    except sqlite3.Error as e:
        return jsonify({'error': f"Database error: {e}"}), 500


def query_states(include_tables, exclude_tables, page_number=1, page_size=50):
    def generate_table_aliases(tables):
        return {table: f"t{idx + 1}" for idx, table in enumerate(tables)}

    include_aliases = generate_table_aliases(include_tables)
    exclude_aliases = generate_table_aliases(exclude_tables)

    sql_query_include = "SELECT DISTINCT s.state FROM solutionsTable s"
    if include_aliases:
        join_clauses_include = [f"JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in
                                include_aliases.items()]
        sql_query_include += " " + " ".join(join_clauses_include)

    sql_query_exclude = None
    if exclude_aliases:
        sql_query_exclude = "SELECT DISTINCT s.state FROM solutionsTable s"
        join_clauses_exclude = [f"LEFT JOIN {table} {alias} ON s.state = {alias}.state" for table, alias in
                                exclude_aliases.items()]
        sql_query_exclude += " " + " ".join(join_clauses_exclude)
        # Asegurar que el registro esté en al menos una tabla
        where_clauses = [f"{alias}.state IS NOT NULL" for alias in exclude_aliases.values()]
        sql_query_exclude += " WHERE " + " OR ".join(where_clauses)

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

        if not os.path.exists(IMAGE_FOLDER):
            os.makedirs(IMAGE_FOLDER)
        else:
            clear_image_folder(IMAGE_FOLDER)

        if missing_states:
            # Ordenar y seleccionar los estados de la página actual
            missing_states_list = sorted(missing_states)
            start_index = (page_number - 1) * page_size
            end_index = start_index + page_size
            page_states = missing_states_list[start_index:end_index]

            placeholders = ','.join('?' * len(page_states))
            sql_details_query = f"""
                SELECT s.state, s.solutions, s.moves 
                FROM solutionsTable s
                WHERE s.state IN ({placeholders})
                ORDER BY s.moves ASC
            """
            cursor.execute(sql_details_query, page_states)
            results = cursor.fetchall()

            result_data = []
            for state, solutions_json, moves in results:
                solutions = json.loads(solutions_json)
                # Generar la imagen para cada estado
                image_filename = generate_image_name(state)
                st2img(state)
                image_url = url_for('static', filename=f'Images/{image_filename}')
                result_data.append({
                    'state': state,
                    'solutions': solutions,
                    'image_url': image_url,
                    'moves': moves
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

    try:
        results_missing_states = query_states(include_tables, exclude_tables, page_number)
    except Exception as e:
            error = str(e)

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
