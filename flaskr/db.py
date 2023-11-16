import sqlite3
import click
from flask import current_app, g
from psycopg2 import extras, connect

def get_db():
    if 'db' not in g:     
            g.db=connect(current_app.config['DB_URL'])
            g.db.cursor_factory = extras.DictCursor          
    return g.db

def close_db(e=None):
    db= g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
 
    with current_app.open_resource("psqlSchema.sql") as f:
        sql_statements = f.read().decode("utf8").split(';')
        sql_statements = [statement.strip() for statement in sql_statements if statement.strip()]
        sqlcur=db.cursor()
        for statement in sql_statements:
            sqlcur.execute(statement)
        sqlcur.close()  
        db.commit()
                  


@click.command("init-db")
def init_db_command(): 
    init_db() 
    click.echo("Initialized the database")     
            

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)



