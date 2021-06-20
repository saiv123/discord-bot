import sqlite3

class BotDB():
    def __init__(self, db_name='botDB'):
        self.db_name = db_name[:db_name.find('.')] if '.' in db_name else db_name
    def __enter__(self):
        self.connection = sqlite3.connect(f'{self.db_name}.db')
        self.cursor = self.connection.cursor()
        return self
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.cursor.close()
        self.connection.close()
        del self.cursor, self.connection

if __name__ == '__main__':
    # Use the context manager to list all tables
    with BotDB() as db:
        db.cursor.execute('''SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name NOT LIKE 'sqlite_%' ''')
        print('Tables:\n'+'\n'.join(db.cursor.fetchall()))
    # Very convenient
    