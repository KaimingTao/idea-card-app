import sqlite3
import uuid
from pathlib import Path
import ast


def create_db(name):
    path = Path(name)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            uuid TEXT PRIMARY KEY,
            name TEXT,
            text TEXT,
            text_type TEXT,
            comment TEXT
        )
    ''')
    conn.commit()
    conn.close()


def insert_idea(db_path, name, text, text_type, comment=""):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO ideas (uuid, name, text, text_type, comment)
        VALUES (?, ?, ?, ?, ?)
    ''', (str(uuid.uuid4()), name, text, text_type, comment))

    conn.commit()
    conn.close()


def get_idea(db_path, name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(f'SELECT text FROM ideas WHERE name = "{name}";')

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None


def get_all_idea(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(f'SELECT text FROM ideas;')
    for i in cursor.fetchall():
        yield i


def get_function_code(file_path, function_name):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            lines = source.splitlines()
            function_lines = lines[start_lineno:end_lineno]
            return "\n".join(function_lines)

    return None


def get_all_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            lines = source.splitlines()
            function_lines = lines[start_lineno:end_lineno]
            yield node.name, 'function', "\n".join(function_lines)

    return None


def get_all_imports(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()
        tree = ast.parse(source)

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            lines = source.splitlines()
            function_lines = lines[start_lineno:end_lineno]
            yield 'import', "\n".join(function_lines)
        elif isinstance(node, ast.ImportFrom):
            start_lineno = node.lineno - 1
            end_lineno = node.end_lineno
            lines = source.splitlines()
            function_lines = lines[start_lineno:end_lineno]
            yield 'import', "\n".join(function_lines)


def work():
    db_name = 'ideas.sqlite'
    create_db(db_name)

    # for code_type, code in get_all_imports(__file__):
    #     insert_idea(db_name, '', code_type, code)


    # for name, code_type, code in get_all_functions(__file__):
    #     insert_idea(db_name, name, code)

    content = list(get_all_idea(db_name))
    with open('test_file.py', 'w') as fd:
        for i in content:
            fd.write(i['text'])
            fd.write('\n\n')


if __name__ == "__main__":
    work()
