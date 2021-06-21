import sqlite3
import json

DB_NAME = 'botDB.db'

def move_json():
    with BotDB(db_name="msg.db") as db:
        data = json.load(open("..\msg.json"))
        for key in data: 
            db.execute(f'CREATE TABLE IF NOT EXISTS {key} (list TEXT PRIMARY KEY NOT NULL)')
            typeM = data[key]
            db.execute(f'DELETE FROM {key}') #deletes all rows from table
            for msg in typeM:
                db.execute(f'INSERT INTO {key} VALUES (?)',(str(msg),))

def add_to_table(key: str, DBname: str, value: str):
    with botDB(db_name=DBname) as db:
        db.execute(f'CREATE TABLE IF NOT EXISTS {key} (value TEXT PRIMARY KEY NOT NULL)')
        db.execute(f'INSERT INTO {key} VALUES (?)',(value,))

def del_table_rows(key: str, DBname: str):
    with botDB(db_name=DBname) as db:
        db.execute(f'DELETE FROM (?)',(key,))

class BotDB():
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name[:db_name.find('.')] if '.' in db_name else db_name
    def __enter__(self):
        self.connection = sqlite3.connect(f'{self.db_name}.db')
        self.cursor = self.connection.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()
        del self.cursor, self.connection

if __name__ == '__main__':
    move_json()
    # Use the context manager to list all tables
    with BotDB() as db:
        db.execute('''SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ''')
        print('Tables:\n'+'\n'.join([x[0] for x in db.fetchall()]))
    # Very convenient
