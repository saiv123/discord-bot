from typing import Any
NoneType = type(None)
import sqlite3
import time
import ast

'''
Written by Leon Leibmann (github.com/Pop101)
In development, Use only with express permission until release
'''

DEFAULT_PATH = './database.db'
class Database():
    
    def __init__(self, path=DEFAULT_PATH) -> None:
        self.path = path
        self.last_result = None

    def execute(self, command:str, args:tuple=None, result_limit:int = -1) -> tuple:
        conn = sqlite3.connect(self.path)
        c = conn.cursor()

        if args == None: args = tuple()

        c.execute(command, args)
        if result_limit < 0: self.last_result = c.fetchall()
        else: self.last_result = c.fetchmany(result_limit)

        conn.commit()
        
        c.close()
        conn.close()
        return self.last_result

    def create_table(self, name:str, columns:dict, hidden_columns:dict or None={'last_modified': float, 'times_modified': int}, key_index:int = 0):
        '''
        columns is dict with keys of names and values of types:
        {
            'name': str,
            'count': int
        }

        If key_index is -1, mark no key
        '''
        if name.lower() == 'table':
            raise ValueError('Table name cannot be "table" or any uppercase variation thereof')
        
        def convert(pytype:type) -> str:
            if pytype == int: return 'integer'
            elif pytype == str: return 'text'
            elif pytype == float: return 'real'
            elif DBLiteral.is_literal(pytype): return 'text'
            else: raise ValueError(f'{pytype} not supported in database') # TODO: use pickle
        
        if hidden_columns:
            columns = {**columns, **hidden_columns}

        columns = [f'[{k}] {convert(v)} NOT NULL' for k, v in columns.items()]
        
        if 0 <= key_index <= len(columns):
            columns[key_index] = columns[key_index] + ' PRIMARY KEY'

        self.execute(f'''CREATE TABLE IF NOT EXISTS {name} ({', '.join(columns)})''')
        return Table(name, path=self.path, bypass_check=True, hidden_columns = ([name for name, _  in hidden_columns.items()] if hidden_columns else None))

    def fetch_tables(self) -> list:
        return [Table(tb_name, path=self.path, bypass_check=True) for _, tb_name, _, _, _, in self.execute('''SELECT * FROM sqlite_master WHERE type='table' ''')]

    def clean(self, timeframe:float=3*30*24*3600) -> None:
        cutoff = time.time() - timeframe

        for table in self.fetch_tables():
            try: self.execute(f'''DELETE FROM {table} WHERE last_modified < {cutoff}''')
            except: pass # ignore cases where last_modified does not exist
    
class Table():
    def __init__(self, name, path=DEFAULT_PATH, bypass_check:bool = False, support_indicies:bool = True, hidden_columns:list=['last_modified', 'times_modified']) -> None:
        self.name = name
        self.database = Database(path=path)
        
        if not bypass_check and not name in self.database.fetch_tables():
                raise Exception(f'Tried to construct Table {name} which is not in database {path}')
        
        self.key = (None, NoneType)
        self.hidden_columns = hidden_columns
        self.support_indicies = support_indicies
        self.columns = self.fetch_columns()

        # Filter out all unused hidden column names
        self.hidden_columns = list(filter(lambda x: x in self.columns.keys(), hidden_columns))
    
    def fetch_columns(self, show_hidden_columns:bool = False, scan_for_dbobjects:bool = True) -> list:
        columns = self.database.execute(f'PRAGMA table_info({self.name})')
        
        # Define function for converting sqlite types to python types
        def convert(sqltype:str, colname:str=None) -> type:
            sqltype = str(sqltype).lower()
            if 'integer' in sqltype: return int
            elif 'real' in sqltype: return float
            elif 'varchar' in sqltype: return str
            elif 'blob' in sqltype: return str
            elif 'text' in sqltype:
                if colname and scan_for_dbobjects: # Check for DBObjects (if we have enough info)
                    finds = self.database.execute(f'''SELECT {colname} FROM {self.name} WHERE {colname} LIKE "%{DBLiteral.PREFIX}%" LIMIT 1''')
                    if finds and len(finds) > 0:
                        return type(DBLiteral(finds[0][-1]).evaluate())
                return str
            else: return NoneType
        
        # Search for and update primary key
        key = [(x[1], convert(x[2])) for x in columns if x[5] == 1]
        self.key = key[0] if len(key) > 0 else None
        
        # Filter out raw column information
        self.raw_columns = {x[1]: convert(x[2], colname=str(x[1])) for x in columns}
        
        # Remove all hidden columns
        self.columns = self.raw_columns.copy()
        for hidden_column in self.hidden_columns:
            try: del self.columns[hidden_column]
            except ValueError: pass

        return self.columns.copy() if show_hidden_columns else self.raw_columns.copy()
    
    def fetch_entries(self, conditions:list or str = None, show_hidden_columns:bool = False, limit:int = -1, offset:int = 0) -> list:
        # Parse conditions.
        # If they're a list, merge them into a string
        # Don't leave it at None under any circumstance
        if conditions:
            if isinstance(conditions, list) or isinstance(conditions, tuple):
                conditions = ' AND '.join(conditions)
            conditions = f' WHERE {conditions}'
        else: conditions = ''
        
        if not limit or limit < 0: limit = f'LIMIT (SELECT Count(1) FROM {self.name})'
        elif limit == 0: return list()
        elif isinstance(limit, int): limit = f'LIMIT {limit}'
        else: raise ValueError('Limit not an integer')

        # Run sql query
        rows = self.database.execute(f'SELECT * FROM {self.name} {conditions} {limit} OFFSET {offset}') #TODO: add space

        # Parse all string entries that are identified as DBLiterals
        rows = list(rows)
        for i in range(len(rows)):
            rows[i] = list(rows[i])
            for j in range(len(rows[i])):
                if DBLiteral.is_representation(rows[i][j]):
                    rows[i][j] = DBLiteral(rows[i][j]).evaluate()

        # Parse all entries into dicts AND filter out all hidden columns
        col_names = list(self.raw_columns.keys())
        if show_hidden_columns:
            entries = [{col_names[i]: row[i] for i in range(len(row))} for row in rows]
        else:
            entries = [{col_names[i]: row[i] for i in range(len(row)) if col_names[i] not in self.hidden_columns} for row in rows]
        return entries
        
    def add_entries(self, rows:list) -> bool:
        for row in rows:
            self.add_entry(row)
        return True

    def add_entry(self, values:dict, key:str = None, fill_missing_values:bool=False) -> bool:
        if not key == None and key not in values:
            raise ValueError('Given key not present in values')
        
        def get_default_value(pytype:type):
            if pytype == str: return ''
            elif pytype == int: return 0
            elif pytype == float: return 0.0
            elif DBLiteral.is_literal(pytype): return f'{DBLiteral.PREFIX}None'
        
        # Before adding, grab previous hidden values if existant
        override_values = dict()
        if key: # skip if key is none
            row = self.database.execute(f'''SELECT {','.join(self.hidden_columns)} FROM {self.name} WHERE {key}={repr(values[key])}''')
            if row and len(row) > 0:
                override_values = {self.hidden_columns[i]: row[0][i] for i in range(len(self.hidden_columns))}

        # Go over everything that should be in values. Validate and add to ordered list
        value_list = list()
        for k, v in self.raw_columns.items():
            # If value isn't given
            if k not in values:
                if k in self.hidden_columns:
                    if 'last_modified' in k: values[k] = time.time()
                    elif k in override_values: 
                        if k in 'times_modified': values[k] = int(override_values[k])+1
                        else: values[k] = override_values[k]
                    else: values[k] = get_default_value(v)
                
                # If ommitted and shouldn't fill
                elif not fill_missing_values:
                    raise ValueError(f'Values given do not match columns: {self.columns}')
                
                else:
                    values[k] = get_default_value(v)
            
            # Now, make sure value's type is okay
            if not (isinstance(values[k], v) or isinstance(values[k], v) or DBLiteral.is_literal(values[k])):
                raise ValueError(f'Given value {k}: {values[k]} does not match expected type {v}')
            
            if DBLiteral.must_parse(values[k]):
                values[k] = repr(DBLiteral(values[k]))
            
            # Finally, store the new value in a list
            # This is so that the final list is in the same order of the table headers
            value_list.append(values[k])
        
        # replace into to table, using python sqlite3's default anti-inject
        if key:
            if self.__contains__(key):
                self.database.execute(f'''UPDATE {self.name} SET ({', '.join([f'{self.raw_columns[x][0]}=(?)' for i in range(len(value_list))])}) WHERE {key}={repr(values[key])}''', tuple(value_list))
            else:
                self.database.execute(f'''REPLACE INTO {self.name} VALUES ({', '.join(['?']*len(value_list))})''', tuple(value_list))
        else: 
            self.database.execute(f'''REPLACE INTO {self.name} VALUES ({', '.join(['?']*len(value_list))})''', tuple(value_list))
        return True
    
    def remove_entry(self, conditions:str or list) -> bool:
        return self.remove_entries(conditions, limit = 1)

    def remove_entries(self, conditions:str or list, limit:int or str = -1) -> bool:
        # Vulnerable to SQL injects
        if isinstance(conditions, list) or isinstance(conditions, tuple):
            conditions = ' AND '.join(conditions)
        
        self.database.execute(f'''DELETE FROM {self.name} WHERE {conditions}''')
        return True
    
    def fetch_by_key(self, key:Any) -> dict:
        return self.__getitem__(key, key_is_index=self.key[1] != int)

    def set_by_key(self, key:Any) -> dict:
        return self.__setitem__(key, key_is_index=self.key[1] != int)
    
    def del_by_key(self, key:Any) -> dict:
        return self.__delitem__(key, key_is_index=self.key[1] != int)
    
    def __len__(self):
        return int(self.database.execute(f'SELECT COUNT(1) FROM {self.name}')[0][0])
    
    def __contains__(self, object:Any):
        if DBLiteral.must_parse(object): object = DBLiteral(object).as_string()
        results = self.database.execute(f'''SELECT COUNT(1) FROM {self.name} WHERE {self.key[0]}={repr(object)} LIMIT 1''')
        return results[0][0] > 0
        
    def __getitem__(self, key:int or Any, key_is_index:bool=None):
        if not (isinstance(key, int) or isinstance(key, self.key[1])): raise ValueError(f'''Key must be integer or {self.key[1]} (type of table's primary key)''')
        if not self.support_indicies: key_is_index = False
        
        if isinstance(key, int) and key_is_index != False:
            if self.key[1] == int and key_is_index != True: raise ValueError(f'''Table's primary key is an integer, making __getitem__'s arguement ambiguous. Use fetch_by_key, call manually with kwargs, or set table.supports_indicies top false''')
            
            results = self.fetch_entries(limit=1, offset=key)
            if len(results) == 0: raise IndexError(f'Given index {key} must be between 0 and table length')
            return results[0]
        else:
            parsed_key = DBLiteral(key).as_string() if DBLiteral.must_parse(key) else key
            results = self.fetch_entries(conditions=[f'{self.key[0]}={repr(parsed_key)}'], limit=2)
            if len(results) == 0: raise NotFound(f'No table item of {key} found in table')
            if len(results) > 1: raise AmbiguousKey('Two or more rows with the given key {key} found')
            return results[0]
    
    def __setitem__(self, key:int or Any, values:dict, key_is_index:bool=None):
        if not (isinstance(key, int) or isinstance(key, self.key[1])): raise ValueError(f'''Key must be integer or {self.key[1]} (type of table's primary key)''')
        if not (isinstance(values, dict) or isinstance(values, list) or isinstance(values, tuple)): raise ValueError(f'''Value to be set must be a dictionary''')
        
        if not self.support_indicies: key_is_index = False
        
        # If it's a list or a tuple, shove it into a dict. This isn't proper though.
        if isinstance(values, list) or isinstance(values, tuple):
            if len(values) < len(self.columns): raise ValueError(f'''List of values must match or exceed length of columns''')
            values_list = list(values)
            values = {self.columns[x][1]: values_list.pop(0) for x in range(len(self.columns))} # Fill in columns
            for x in range(len(self.hidden_columns)):
                if len(values_list) == 0: break
                values[self.hidden_columns[x]] = values_list.pop(0)
        
         
        if isinstance(key, int) and key_is_index != False:
            if self.key[1] == int and key_is_index != True: raise ValueError(f'''Table's primary key is an integer, making __setitem__'s arguement ambiguous. Use set_by_key, call manually with kwargs, or set table.supports_indicies top false''')
            
            # If key is an integer, fetch the row there , get it's key, and overwrite it
            # If the key is exactly the object's length, allow adding a row
            if key == len(self):
                self.add_entry(values)
            else:
                results = self.fetch_entries(limit=1, offset=key)
                if len(results) == 0: raise IndexError(f'Given index {key} must be between 0 and table length (inclusive)')
                
                values[self.key[0]] = results[0][self.key[0]]
                self.add_entry(values, self.key[0])
        else:
            if not isinstance(key, self.key[1]): raise ValueError(f'''Given key {key} does not match table key of {self.key[1]}''')
            if DBLiteral.must_parse(key): key = DBLiteral(key).as_string()
            
            # Since we have the key object (self.key[0], key), simply try to overwrite or add
            if len(self.columns) == 1: raise AmbiguousKey('Key cannot be updated')
            values[self.key[0]] = key
            self.add_entry(values, self.key[0])
    
    def __delitem__(self, key:int or Any, key_is_index:bool=None):
        if not (isinstance(key, int) or isinstance(key, self.key[1])): raise ValueError(f'''Key must be integer or {self.key[1]} (type of table's primary key)''')
        if not self.support_indicies: key_is_index = False
        
        if isinstance(key, int) and key_is_index != False:
            if self.key[1] == int and key_is_index != True: raise ValueError(f'''Table's primary key is an integer, making __delitem__'s arguement ambiguous. Use del_by_key, call manually with kwargs, or set table.supports_indicies top false''')
            
            results = self.fetch_entries(limit=1, offset=key)
            if len(results) == 0: raise IndexError(f'Given index {key} must be between 0 and table length')
            
            # We have the full row we must delete, so string together conditions based on it
            conditions = [(x[0], results[0][x[0]]) for x in self.raw_columns if x in results[0]]
            conditions = [f'''{k}={repr(DBLiteral(v).as_string() if DBLiteral.must_parse(v) else v)}''' for k, v in conditions]
            self.remove_entries(conditions)
        else:
            # Since we already have the key, simply delete all rows that match it
            parsed_key = DBLiteral(key).as_string() if DBLiteral.must_parse(key) else key
            self.remove_entries(conditions=[f'{self.key[0]}={repr(parsed_key)}'])
    
    def __repr__(self):
        return f'''<Table "{self.name}" in database {self.database.path}>'''
            
class DBLiteral():
    PREFIX = 'DBLiteral '
    def __init__(self, object) -> None:
        # Raise exception if it cannot create one
        if not DBLiteral.is_literal(type(object)): raise ValueError(f'Cannot parse {object} to literal')
        
        # When importing from db, check if it already has the prefix
        if isinstance(object, str) and str(object).startswith(DBLiteral.PREFIX):
            self.object = str(object)[len(DBLiteral.PREFIX):]
        else:
            self.object = repr(object)

    def evaluate(self) -> Any:
        if self.object == f'None': return None
        return ast.literal_eval(self.object)
    
    def as_string(self) -> str:
        return repr(self)
    
    def __repr__(self) -> str:
        return f'{DBLiteral.PREFIX}{self.object}'
    
    def __str__(self) -> str:
        return self.object
    
    @staticmethod
    def is_literal(_type:type) -> bool:
        if _type in (None, NoneType): return True
        if not isinstance(_type, type): _type = type(_type)
        return _type in (int, bool, str, float, list, tuple, set, dict, ast.Constant, ast.FormattedValue, ast.JoinedStr, ast.List, ast.Tuple, ast.Set, ast.Dict, None, NoneType)
    
    @staticmethod
    def must_parse(_type:type) -> bool:
        if _type in (None, NoneType): return True
        if not isinstance(_type, type): _type = type(_type)
        return _type in (list, tuple, set, dict, ast.List, ast.Tuple, ast.Set, ast.Dict, None, NoneType)
    
    @staticmethod
    def is_representation(obj:Any) -> bool:
        if isinstance(obj, str):
            str_obj = str(obj)[len(DBLiteral.PREFIX):] if str(obj).startswith(DBLiteral.PREFIX) else str(obj)
            try: 
                ast.literal_eval(str_obj)
                return True
            except:
                return False
        return False

class NotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class AmbiguousKey(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Configuration(Table):
    KEY_COLUMN_NAME = 'ID'
    def __init__(self, name:str, default_settings:dict, path = DEFAULT_PATH, setting_type_overrides:dict=dict()) -> None:
        '''
        settings is the same as columns, a list of tuples containing (varname:str, vartype:type)
        TODO: add defaults
        '''
        self.defaults = default_settings.copy()

        for k, v in default_settings.items():
            default_settings[k] = type(v)

        # Insert guild id into options
        settings = {**{Configuration.KEY_COLUMN_NAME: int}, **default_settings, **setting_type_overrides}

        # Create new table and initialize self
        Database(path=path).create_table(name, settings)
        super(Configuration, self).__init__(name, path = path, bypass_check=True, support_indicies=False)
    
    def get(self, key:Any or int, setting:str) -> Any:
        settings = self.get_all(key)
        return settings[setting]
    
    def get_all(self, key:Any or int) -> dict:
        key = Configuration.extract_id(key)
        if not isinstance(key, int): raise ValueError('Guild given is not a discord.Guild, discord.User or discord id')

        results = self.fetch_entries(conditions=[f'{Configuration.KEY_COLUMN_NAME}={key}'], limit=1)
        if results and len(results) > 0:
            del results[0][Configuration.KEY_COLUMN_NAME]
            return results[0]
        else:
            return self.defaults
    
    def set(self, key:Any or int, setting:str, value:Any):
        key = Configuration.extract_id(key)
        if not isinstance(key, int): raise ValueError('Guild given is not a discord.Guild, discord.User or discord id')

        if setting not in self.columns: raise ValueError(f'Setting {setting} not found in table {self.name}')
        
        try: has_set = self.database.execute(f'''SELECT {Configuration.KEY_COLUMN_NAME} FROM {self.name} WHERE {Configuration.KEY_COLUMN_NAME}={key} LIMIT 1''')
        except: has_set = False

        if has_set:
            if DBLiteral.must_parse(value): value = DBLiteral(value).as_string()
            self.database.execute(f'''UPDATE {self.name} SET {setting}={repr(value)} WHERE {Configuration.KEY_COLUMN_NAME}={key}''')
        else:
            self.add_entry({**self.defaults, **{Configuration.KEY_COLUMN_NAME: key, setting: value}})
    
    def set_all(self, key:Any or int, settings:dict):
        key = Configuration.extract_id(key)
        if not isinstance(key, int): raise ValueError('Guild given is not a discord.Guild, discord.User or discord id')

        try: has_set = self.database.execute(f'''SELECT {Configuration.KEY_COLUMN_NAME} FROM {self.name} WHERE {Configuration.KEY_COLUMN_NAME}={key} LIMIT 1''')
        except: has_set = False

        if has_set:
            setting_str = list()
            for setting, value in settings.items():
                if setting not in self.columns: raise ValueError(f'Setting {setting} not found in table {self.name}')
                if DBLiteral.must_parse(value): value = DBLiteral(value).as_string()
                setting_str.append(f'{setting}={repr(value)}')
            setting_str = ', '.join(setting_str)

            self.database.execute(f'''UPDATE {self.name} SET {setting_str} WHERE {Configuration.KEY_COLUMN_NAME}={key}''')
        else:
            self.add_entry({**self.defaults, **settings})
    
    def is_set(self, key: Any) -> bool:
        key = Configuration.extract_id(key)
        return super().__contains__(key)
    
    def is_changed(self, key: Any) -> bool:
        return self.get_all(key) != self.defaults
    
    def __contains__(self, object: Any) -> bool:
        return True # The entire point is to contain everything (because of the set defaults). Use is_set or is_changed
    
    def __getitem__(self, key: int or Any) -> dict:
        return self.get_all(key)
    
    def __setitem__(self, key: int or Any, values: dict,):
        key = Configuration.extract_id(key)
        return super().__setitem__(key, values, key_is_index=False)
    
    def __delitem__(self, key: int or Any):
        key = Configuration.extract_id(key)
        return super().__delitem__(key, key_is_index=False)
    
    @staticmethod
    def extract_id(obj:Any, allow_none:bool=False) -> int:
        try: return int(obj)
        except: pass
        
        attributes = ['id', 'hash', 'int']
        for attribute in attributes:
            if hasattr(obj, attribute):
                attribute = getattr(obj, attribute)
                if isinstance(attribute, int):
                    return obj.id
                else:
                    return hash(attribute)
                
        if not allow_none:
            raise ValueError('''Cannot extract identifier from object. It must have 'id' or similar as a property''')
        else:
            return hash(obj)
        
if __name__ == '__main__':
    config = Configuration("Tabled", {
        'nickname': 'NoNicknameNancy',
        'power': 100,
        'friends': ['juan', 'juanita']
    })
    print(config.get(1, 'nickname'))
    print('friends', config.get(1, 'friends'),'\n\n')

    config.set(1, 'nickname', 'bobert')
    print(config.get(1, 'nickname'),'\n\n')

    config.set(1, 'friends', ['jack', 'jill'])
    print('name', config.get(1, 'nickname'))
    print('friends', config.get(1, 'friends'))

    # 26 bugs squashed
    
    # Now, test out raw table access
    db = Database()
    table = db.create_table('TeePoser', {'uid':str, 'description': str})
    print('all tables in db:', db.fetch_tables())
    print('table length:', len(table))
    if len(table) > 0: print('table[0]:', table[0])
    print('\n')
    
    print('setting table[0]...')
    table[0] = {'uid': '1', 'description': 'juan'}
    print('table[0]:', table[0],'\n')
    
    print('setting table["juan"]...')
    table['1'] = {'uid': '1', 'description': 'joeseph'}
    print('table[0]:', table[0])
    print('table["1"]:', table['1'],'\n')
    
    # 6 bugs squashed
    
    # Merge functionality
    print(config.fetch_entries(),'\n')
    print(config[1],'\n')