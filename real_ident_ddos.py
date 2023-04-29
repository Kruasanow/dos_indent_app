from pyshark import FileCapture
import asyncio

UPLOAD_FOLDER = 'dump_input/'
ALLOWED_EXTENSIONS = set(['pcap','pcapng'])

def get_file(name_of_file=None):
    cap = []
    if name_of_file == None:
        print('[*]osh.py: nothing choosed')
    try:
        full_way = 'dump_input/'+str(name_of_file)
        print('[*]osh.py: full way - ' +str(full_way))
        cap = FileCapture(full_way)
        asyncio.get_child_watcher().attach_loop(cap.eventloop)
        print('[*]osh.py: cap for pyshark - ' +str(cap))

    except Exception:
        print('[*]osh.py: get_file - exceptions worked...')
    return cap


def get_dname_from_db():
    good_dname = ''
    from db_do.conn_db import get_db_connection
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT dname FROM dump_list;')
        case1 = cur.fetchall()
        cur.close()
        conn.close()
        good_dname = str(case1[-1]).translate({
                                    ord("'"): None, 
                                    ord("("): None,
                                    ord(")"): None,
                                    ord(","): None
                                    })
        print('[*]osh.py element choosed - ' + good_dname)
    except Exception:
        print('[*]osh.py: bad get dname!')
    return good_dname

def add_dump(dname):
    from db_do.conn_db import get_db_connection
    print('[*]dns_db_addiction.py: dump name - '+str(dname))
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO dump_list (dname) VALUES (%s)',[dname])
    conn.commit()
    cur.close()
    conn.close()

def current_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# cap = get_file(get_dname_from_db())
