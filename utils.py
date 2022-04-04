import sqlite3
from os.path import join as join_path

USERS = ['admin', 'test']
SEARCH_RESULTS = (
    ('Twitter', 'twitter', 'https://twitter.com'),
    ('Google', 'google', 'https://google.com.au'),
    ('Apple', 'apple website', 'https://apple.com.au'),
)


def get_source_code(path: str, _range=None):
    fp = join_path(path)
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()
    if _range is None:
        return ''.join(lines)
    else:
        if len(_range) != 2:
            raise ValueError(f"expect _range to be 2, got {len(_range)}")
        # make range inclusive
        lo = _range[0] - 1
        hi = _range[1] + 1
        return ''.join(lines[lo:hi])


def mk_route_struct(name: str, desc, **kwargs):
    route = name.lower().strip().replace(' ', '-')
    template_name = route.replace('-', '_')
    return {
        route: {
            'name': name,
            'route': route,
            'description': desc,
            'template': f'{template_name}.html',
            'variables': {
                **kwargs
            },
        }
    }


def init_db():
    db_conn = sqlite3.connect('./database.sqlite3')
    db_conn.execute("""CREATE TABLE IF NOT EXISTS xss_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post TEXT NOT NULL);""")
    db_conn.commit()

    db_conn.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL);""")
    db_conn.commit()

    cursor = db_conn.execute("SELECT count(*) from users;")
    res = cursor.fetchall()
    if res[0][0] == 0:
        for user in USERS:
            db_conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?);",
                (user, "password"),
            )
        db_conn.commit()
    else:
        db_conn.execute("UPDATE users SET password='password';")
        db_conn.commit()

    db_conn.execute("""CREATE TABLE IF NOT EXISTS sqli_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL);""")
    db_conn.commit()
    db_conn.execute("DELETE from sqli_table;")
    db_conn.commit()
    for result in SEARCH_RESULTS:
        db_conn.execute(
            "INSERT INTO sqli_table (name, description, url) VALUES (?, ?, ?);",
            result,
        )
    db_conn.commit()
    db_conn.close()