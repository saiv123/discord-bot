import sqlite3

DB_NAME = 'botDB.db'

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
    # Use the context manager to list all tables
    with BotDB() as db:
        db.execute('''SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ''')
        print('Tables:\n'+'\n'.join([x[0] for x in db.fetchall()]))
    # Very convenient
    