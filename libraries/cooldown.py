import discord
import ast, time
import sqlite3
import inspect

import botDB
from helperFunctions import isOwner

# Create table in database
with botDB.BotDB() as db:
    db.execute('''CREATE TABLE IF NOT EXISTS COOLDOWNS ([user] TEXT PRIMARY KEY NOT NULL, [lastused] date NOT NULL, [data] TEXT NOT NULL)''')

class UserCooldownException(Exception):
    # User: the discord.User or other way to keep track of the user
    # Command: the category used
    # tl: time left
    # mt: max time
    # x: times the command can be used
    def __init__(self, user, command='', tl=0, mt=0, x=0):
        self.user = user
        self.command = command
        self.tl = tl
        self.mt = mt
        self.x = x
    
    def time_left_msg(self):
        if self.tl and self.mt:
            return f'{self.tl}s of {self.mt}s'
        return 'Unknown time left'
    
    def law_msg(self):
        if self.mt and (not self.x or self.x == 1):
            return f'Once every {self.mt}s'
        elif self.x:
            return f'{self.x} times every {self.mt}s'
        return 'Unknown'

    def get_msg(self, give_time_left:bool=True, give_command_law:bool=True):
        usr = self.user.name if isinstance(self.user, discord.User) else repr(self.user)
        tim = f' {self.time_left_msg()}s left'; tim = '' if 'unknown' in tim.lower() or not give_time_left else tim
        law = f' Can be used {self.law_msg()}'; law = '' if 'unknown' in law.lower() or not give_command_law else law
        return f'{usr}{tim}{law}'
    
    def __str__(self):
        return self.get_msg()

def clean(days=30): # If you don't use a command with a cooldown in 30 days, you get purged
    conn = sqlite3.connect(botDB.DB_NAME); cursor = conn.cursor()
    cursor.execute(f'''DELETE FROM COOLDOWNS WHERE lastused < date('now','-{days}days')''')
    conn.commit(); cursor.close(); conn.close()

def force_use_cmd(user:discord.User or str, command:str):
    '''
    Uses a command. Ignores all cooldown, but records information
    '''
    if isinstance(user, discord.User): user = user.id; user = str(user)
    conn = sqlite3.connect('botDB.db'); cursor = conn.cursor()

    # Get and parse user info from table
    cursor.execute(f'SELECT * FROM COOLDOWNS WHERE user = (?)',(str(user),))
    user_rows = cursor.fetchall()
    user_info = ast.literal_eval(user_rows[0][2]) if len(user_rows) > 0 else dict()

    if not isinstance(user_info, dict): raise Exception(f'Incorrect entry in COOLDOWNS table for user {user}')
    if command in user_info:
        user_info[command]['last_use'] = int(time.time())
        user_info[command]['times_used'] = 1 + int(user_info[command]['times_used'])
    else:
        user_info[command] = {
            'last_use': int(time.time()),
            'times_used': 1,
            'first_use': int(time.time())
        }

    cursor.execute('''REPLACE INTO COOLDOWNS VALUES (?, date('now'), ?)''', (str(user), str(user_info)))
    conn.commit(); cursor.close(); conn.close()

def use_cmd(user:discord.User or str, command:str, cooldown:float, uses=1, use_first_use:bool=False):
    '''
    Uses a command, raising an exception if it is on cooldown
    '''
    if isinstance(user, discord.User): user = user.id; user = str(user)
    conn = sqlite3.connect(botDB.DB_NAME); cursor = conn.cursor()

    # Get and parse user info from table
    cursor.execute(f'SELECT * FROM COOLDOWNS WHERE user = (?) ',(str(user),))
    user_rows = cursor.fetchall()
    user_info = ast.literal_eval(user_rows[0][2]) if len(user_rows) > 0 else dict()

    if not isinstance(user_info, dict): raise Exception(f'Incorrect entry in COOLDOWNS table for user {user}')
    if command in user_info:
        # Check for cooldown
        last_for_cooldown_purposes = user_info[command]['first_use'] if use_first_use else user_info[command]['times_used']
        if time.time() < cooldown + last_for_cooldown_purposes and user_info[command]['times_used'] >= uses:
            raise UserCooldownException(user, command, tl=cooldown-(time.time()-last_for_cooldown_purposes), mt=cooldown, x=uses)
        
        # If we've ellapse the entire cooldown since last use, reset first use
        if time.time() > cooldown + user_info[command]['last_use']:
            user_info[command]['first_use'] = int(time.time())
        
        user_info[command]['last_use'] = int(time.time())
        user_info[command]['times_used'] = 1 + int(user_info[command]['times_used'])
    else:
        user_info[command] = {
            'last_use': int(time.time()),
            'times_used': 1,
            'first_use': int(time.time())
        }

    cursor.execute('''REPLACE INTO COOLDOWNS VALUES (?, date('now'), ?)''', (str(user), str(user_info)))
    conn.commit(); cursor.close(); conn.close()

# Use this wrapper to add cooldowns
def has_cooldown(cooldown:float, times:int=1, category:str='', use_first_use:bool=False, admin_exempt:bool=False, owner_exempt:bool=False):
    def wrapper(func):
        cmd_name = category if len(category) == 0 else func.__name__
        has_kwargs = not '=' in str(inspect.signature(func))
        
        def wrap(*args, **kwargs):
            user = args[1].author
            if (isOwner(user) and owner_exempt) or (user.guild_permissions.administrator and admin_exempt):
                force_use_cmd(user, cmd_name)
            else:
                use_cmd(user, cmd_name, cooldown, uses=times, use_first_use=use_first_use)
            return func(*args,**kwargs)
        
        if not has_kwargs:
            def wrap_(*args):
                return wrap(*args)
            return wrap_
        return wrap
    return wrapper