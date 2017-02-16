"""

This module wraps the SQL functionality and uses SQLite to access a database

Todo:
    - Insert/Update/Delete for entries
    - multiple cursors and connections to different tables and databases
"""

import sqlite3
import time
import datetime
import random


_conn = 0
_cursor = 0


def create_table():
    """ Just a temporary test function to create a table"""
    _cursor.execute("CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamt TEXT, keyword TEXT, value REAL)")


def data_entry():
    """ Just a temporary test function to create data in a table"""
    _cursor.execute("INSERT INTO stuffToPlot VALUES(1342324233, '2016-12-10','Python',6)")
    _cursor.execute("INSERT INTO stuffToPlot VALUES(1342323433, '2016-12-11','Python',7)")
    _cursor.execute("INSERT INTO stuffToPlot VALUES(1342364533, '2016-12-12','Python',8)")
    _conn.commit()
    _cursor.close()
    _conn.close()


def open_database(database):
    """ This function will create a connection to a SQLite database

    Args:
        database: Name/Path of the SQLite database file
    """
    global _conn
    global _cursor

    _conn = sqlite3.connect(database)
    _cursor = _conn.cursor()


def close_database():
    """ This function will close the connection to a SQLite database and its cursor"""
    global _conn
    global _cursor

    _conn.commit()
    _cursor.close()
    _conn.close()


def commit_database():
    """" This function will trigger a commit to the currently used database """
    global _conn
    _conn.commit()


def create_new_table(tablename, field_type_tupel, check_existance=True, **keyargs):
    """ This function will create a new table in the currently opened DB

    Args:
        tablename:        Name of the table to be created
        field_type_tupel: List of tupels of Fieldname and SQLite datatype in the table [(field1,type1),...]
        check_existance:  Check if table exists before creating, default==True
        **keyargs:        [Not in use yet]"""

    print("Table to be created: {}".format(tablename))

    create_statement = "CREATE TABLE "
    if check_existance:
        create_statement += "IF NOT EXISTS "
    create_statement += tablename + "("

    for count, tupel in enumerate(field_type_tupel):
        create_statement += tupel[0] + " " + tupel[1]
        if count < (len(field_type_tupel) - 1):
            create_statement += ", "
    create_statement += ")"

    print(create_statement)

