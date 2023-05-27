import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="petr_db",
        user='petrov',
        password='petrov'
        )

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS dns_srv_profile;')
cur.execute('CREATE TABLE profile (id serial PRIMARY KEY,'
                                 'ip varchar (50),'# #
                                 'dns varchar (40),'
                                 'data varchar (40),'
                                 'icmp varchar (40),'# #
                                 'ssl varchar (40),'
                                 'tcp varchar (40),'
                                 'udp varchar (40),'
                                 'llp varchar (40),'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

cur.execute('DROP TABLE IF EXISTS dump_list;')
cur.execute('CREATE TABLE dump_list (id serial PRIMARY KEY, dname varchar (64));') 

conn.commit()

cur.close()
conn.close()

