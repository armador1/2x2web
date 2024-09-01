import random

from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import json
from ScrImg import st2img, generate_image_name, sub_st2img
from TranslatedSolver import fixCorner, TranslateStList
import os
import shutil
import ast
import random as rd
import _2x2Main as Main

app = Flask(__name__)

# Ruta a la carpeta de imágenes
IMAGE_FOLDER = 'static/Images/'
SUBIMAGE_FOLDER = 'static/SubImages/'


def transl_state_id(state):
    try:
        st = ast.literal_eval(state)
    except:
        st = state

    key = ['2cr', '5H2', 'fl7', 'qq!', 'cnp', 'arg', 'jr8', 'mba', 'f08', 'wgi', '99z', 'd23',
           'avo', '196', '9lj', '0ok', 'hd2', 'S11', 'aas', 'c!?', 'lpm', 'bad', 'oz9', '0xl']

    tst = ''
    for i in st:
        tst = tst + key[i - 1]

    return tst


@app.context_processor
def inject_functions():
    return dict(translate_state_id=transl_state_id)


def inv_transl_state_id(tstate):
    key = ['2cr', '5H2', 'fl7', 'qq!', 'cnp', 'arg', 'jr8', 'mba', 'f08', 'wgi', '99z', 'd23',
           'avo', '196', '9lj', '0ok', 'hd2', 'S11', 'aas', 'c!?', 'lpm', 'bad', 'oz9', '0xl']

    key_list = [(tstate[i:i + 3]) for i in range(0, len(tstate), 3)]
    state_id = [0] * 24

    for i in range(0, len(state_id)):
        state_id[i] = key.index(key_list[i]) + 1

    return str(state_id)


def clear_image_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


def rotateSolution(solution):
    rotated_solutions = [solution]
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "x'")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "x'")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "x")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)
    solution = Main.new_orientation(solution, "z")
    rotated_solutions.append(solution)

    rotated_solutions = list(set(rotated_solutions))

    rotated_solutions_str = "\n".join(str(x) for x in rotated_solutions)

    return rotated_solutions_str


@app.route('/info')
def info():
    return render_template('info.html')


def methods_and_labels(state):

    conn = sqlite3.connect('oo.db')
    cursor = conn.cursor()

    tables = ["CLL", "EG1", "EG2", "TCLL", "TEG1", "TEG2", "LS", "LSEG1", "LSEG2", "CBL"]
    methods = []

    for table in tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        methods.append(cursor.fetchone() is not None)

    bar_tables = [f"Bar_{i}" for i in range(9)]

    for table in bar_tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        if cursor.fetchone():
            methods.append(int(table[4:]))

    abar_tables = [f"ABar_{i}" for i in range(7)]

    for table in abar_tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        if cursor.fetchone():
            methods.append(int(table[5:]))

    obar_tables = [f"OBar_{i}" for i in range(9)]
    obar_tables.append("OBar_12")

    for table in obar_tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        if cursor.fetchone():
            methods.append(int(table[5:]))

    diag_tables = [f"Diag_{i}" for i in range(9)]

    for table in diag_tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        if cursor.fetchone():
            methods.append(int(table[5:]))

    adiag_tables = [f"ADiag_{i}" for i in range(7)]

    for table in adiag_tables:
        cursor.execute(f"SELECT 1 FROM {table} WHERE state = '{state}' LIMIT 1")
        if cursor.fetchone():
            methods.append(int(table[6:]))

    conn.close()

    methods2 = [{"condition": methods[tables.index(table)], "label": table, "class": f"bubble-{table}",
                 "is_number": False} for table in tables]
    methods2.append({"condition": methods[10], "label": "Bar", "class": "bubble-bar", "is_number": True})
    methods2.append({"condition": methods[11], "label": "Adj Bar", "class": "bubble-abar", "is_number": True})
    methods2.append({"condition": methods[12], "label": "Opp Bar", "class": "bubble-obar", "is_number": True})
    methods2.append({"condition": methods[13], "label": "Diag", "class": "bubble-diag", "is_number": True})
    methods2.append({"condition": methods[14], "label": "Adj Diag", "class": "bubble-adiag", "is_number": True})

    return methods2


@app.route('/state/<tstate_id>')
def state_details(tstate_id):
    state_id = inv_transl_state_id(tstate_id)
    conn = sqlite3.connect('oo.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT solutions, moves, oo FROM solutionsTable WHERE state = ?", (state_id,))
        result = cursor.fetchone()

        if result:
            solutions_json, moves, oo = result
            solutions = json.loads(solutions_json)
            image_filename = generate_image_name(state_id)
            if not os.path.exists(SUBIMAGE_FOLDER):
                os.makedirs(SUBIMAGE_FOLDER)
            else:
                clear_image_folder(SUBIMAGE_FOLDER)
            shutil.copy(f'static/Images/{image_filename}', 'static/SubImages/')
            image_url = url_for('static', filename=f'SubImages/{image_filename}')

            return render_template('state_details.html',
                                   state=state_id,
                                   solutions=solutions,
                                   image_url=image_url,
                                   moves=moves,
                                   oo=oo,
                                   methods_and_labels=methods_and_labels(state_id))
        else:
            return f"Estado {state_id} no encontrado.", 404

    except sqlite3.Error as e:
        return f"Error al acceder a la base de datos: {e}", 500

    finally:
        conn.close()


@app.route('/get_scramble', methods=['POST'])
def get_scramble():
    csol = request.form.get('solution')
    csol2 = csol.replace('&#34;', '"')
    new_csol = csol2.replace('&#39;', "'")
    solutions = ast.literal_eval(new_csol)
    if len(solutions) == 0:
        return jsonify({'scramble': ''})
    scrb_sol = solutions[rd.randint(0, len(solutions) - 1)]
    scrb1 = scrb_sol.split(' ')
    scrb1.reverse()
    scrb = ""
    for i in scrb1:
        if "'" in i:
            appn = i.replace("'", '')
        elif '2' in i:
            appn = i
        else:
            appn = i + "'"
        scrb = scrb + appn + " "

    scramble = scrb[:-1]
    return jsonify({'scramble': scramble})


@app.route('/update_state', methods=['POST'])
def update_state():
    state_id = request.form.get('state_id')
    rotation = request.form.get('rotation')
    csol = request.form.get('csol')
    csol2 = csol.replace('&#34;', '"')
    new_csol = csol2.replace('&#39;', "'")
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
            rotated_solutions.append(Main.new_orientation(sol, rot2))

        rot = getattr(Main, rotation)
        new_state_id = str(
            fixCorner(TranslateStList(Main.s2sList(rot(Main.sList2s(ast.literal_eval(state_id)))))))
        clear_image_folder(SUBIMAGE_FOLDER)
        image_filename = generate_image_name(new_state_id)
        sub_st2img(new_state_id)

        new_image_url = url_for('static', filename=f'SubImages/{image_filename}')

        return jsonify({'new_image_url': new_image_url,
                        'new_state_id': new_state_id,
                        'solutions': rotated_solutions,
                        'str_solutions': str(rotated_solutions)})

    except sqlite3.Error as e:
        return jsonify({'error': f"Database error: {e}"}), 500


# EL ORDEN CON LOS MOVES NO FUNCIONA BIEN DEBIDO A LA PAGINACIÓN
# LA PAGINACIÓN HACE QUE LA WEB CREA QUE SOLO HAY 50 ESTADOS. CADA VEZ QUE SE PASA DE PÁGINA, SE HACE UNA QUERY NUEVA
# PERO IGNORANDO LOS 50 REGISTROS ANTERIORES.
def query_states(include_tables, exclude_tables, page_number=1, page_size=50):
    def generate_table_aliases(tables):
        return {table: f"t{idx + 1}" for idx, table in enumerate(tables) if table}

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
                SELECT s.state, s.solutions, s.oo
                FROM solutionsTable s
                WHERE s.state IN ({placeholders})
            """
            cursor.execute(sql_details_query, page_states)
            results = cursor.fetchall()

            result_data = []
            for state, solutions_json, oo in results:
                solutions = json.loads(solutions_json)
                try:
                    scramble_moves = Main.Sol2Scr(random.choice(solutions))
                except:
                    scramble_moves = ''
                scramble_moves2 = [move.replace('3', "'") for move in scramble_moves]
                scramble = ' '.join(scramble_moves2)
                # Generar la imagen para cada estado
                image_filename = generate_image_name(state)
                st2img(state)
                image_url = url_for('static', filename=f'Images/{image_filename}')
                result_data.append({
                    'state': state,
                    'scramble': scramble,
                    'image_url': image_url,
                    'oo': oo
                })
            return result_data, len(missing_states_list)
        return []
    except sqlite3.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return []
    finally:
        conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        page_number = 1
        include_tables = request.form.getlist('tables_include')
        exclude_tables = request.form.getlist('tables_exclude')
    else:
        page_number = int(request.args.get('page', 1))
        include_tables = request.args.getlist('tables_include')
        exclude_tables = request.args.getlist('tables_exclude')
    found_states = None
    error = None

    try:
        found_states = query_states(include_tables, exclude_tables, page_number)
    except Exception as e:
        error = str(e)

    return render_template('search.html',
                           results_missing_states=found_states[0],
                           number_results=found_states[1],
                           error=error,
                           page_number=page_number,
                           include_tables=include_tables,
                           exclude_tables=exclude_tables)


@app.route('/scramble_search', methods=['GET', 'POST'])
def search2():
    if request.method == 'POST':
        scramble = request.form.get('scramble')
    super_scramble = rotateSolution(scramble)
    scr_list = super_scramble.split('\n')
    state_list = []
    for i in range(0, len(scr_list)):
        scraux = scr_list[i].split(' ')
        for k in range(0, len(scraux)):
            if "'" in scraux[k]:
                scraux[k] = scraux[k].replace("'", '3')

        try:
            state = Main.Solved()
            for k in scraux:
                move = getattr(Main, k)
                state = move(state)
            state_list.append(Main.s2sList(state))
        except:
            print('Invalid Scramble')

    conn = sqlite3.connect('oo.db')
    cursor = conn.cursor()

    results = None
    for st in state_list:
        cursor.execute(f"SELECT * FROM solutionsTable WHERE state = '{st}' LIMIT 1")
        results = cursor.fetchone()
        if results:
            break

    conn.close()

    found_state = results[0]
    if not os.path.exists(SUBIMAGE_FOLDER):
        os.makedirs(SUBIMAGE_FOLDER)
    else:
        clear_image_folder(SUBIMAGE_FOLDER)
    sub_st2img(found_state)
    image_filename = generate_image_name(found_state)
    image_url = url_for('static', filename=f'SubImages/{image_filename}')

    return render_template('state_details.html',
                           state=found_state,
                           solutions=json.loads(results[1]),
                           image_url=image_url,
                           moves=results[2],
                           oo=results[3],
                           methods_and_labels=methods_and_labels(found_state))


@app.route('/rotate_solution')
def rotate_solution():
    solution = request.args.get('solution', '')
    rotated_solution = rotateSolution(solution)
    return jsonify({'result': rotated_solution})


if __name__ == '__main__':
    app.run()
