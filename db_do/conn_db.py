import os
import psycopg2 as ps

def get_db_connection():
    conn = ps.connect(host='localhost',
                      database='petr_db',
                      user='petrov',
                      password='petrov'
                    )
    return conn