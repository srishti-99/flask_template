import datetime
from pathlib import Path
from os import environ
from configparser import ConfigParser
import pandas as pd
from psycopg2 import connect, Error

class Data():
    def __init__(self, config_file='database.ini', timeout=5):
        self.conn = connector(timeout=timeout) 
        self.df = pd.read_sql_query("SELECT * FROM users", con=self.conn)
        self.df = self.df.set_index('username')

    def update_df(self):
        self.df = pd.read_sql_query("SELECT * FROM users", con=self.conn)
        self.df = self.df.set_index('username')


def insert_user(firstname, lastname, username, description):
    insert_query = """ INSERT INTO users (firstname, lastname, username, description) VALUES (%s,%s,%s,%s);"""
    insert_record = (firstname, lastname, username, description)
    query_psql(query=insert_query, data=insert_record)

def update_user(firstname, lastname, username, description):
    update_query = """UPDATE users SET firstname = %s , lastname = %s , description = %s WHERE username= %s;"""
    update_record = (firstname, lastname, description, username)
    query_psql(query=update_query, data=update_record)

def delete_user(username):
    delete_query = """DELETE FROM users WHERE username = %s ;"""
    delete_record = (username, )
    query_psql(query=delete_query, data=delete_record)

def query_psql(query, data, timeout=5):
    conn = connector(timeout=timeout)
    cur = conn.cursor()
    cur.execute(query, data)
    conn.commit()
    cur.close()
    conn.close()

def connector(configfile='database.ini', env=None, timeout=5):
    config = ConfigParser()
    config.read(configfile)
    if env is None:
        env = environ['FLASK_ENV']

    dbname = config[env]['database']
    user = config[env]['user']
    host = config[env]['host']
    password = config[env]['password']

    conn = connect(
        dbname = dbname,
        user = user,
        host = host,
        password = password,
        # attempt to connect for 5 seconds then raise exception
        connect_timeout = timeout
    )
    return conn
