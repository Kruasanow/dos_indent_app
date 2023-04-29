from pyshark import FileCapture
import asyncio
import matplotlib.pyplot as plt
import datetime
import base64
import io

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

def get_time_grath(a,name,c):
    dns_packets = []

    # Парсинг pcapng-файла и выборка DNS пакетов
    for packet in a:
        if name in packet:
            dns_packets.append(packet)
    # print(dns_packets)

    # Получение времени каждого DNS-запроса
    times = []
    for packet in dns_packets:
        ts = packet.sniff_timestamp
        time = datetime.datetime.fromtimestamp(float(ts))
        times.append(time)

    # print(times)
    # 

    # Создание графика
    fig, ax = plt.subplots()
    ax.plot(times, range(len(times)), label=f'{name} запросы')
    ax.legend()
    ax.set_xlabel('Время')
    ax.set_ylabel(f'Количество {name} запросов')
    ax.set_title(f'График {name} запросов')
    plt.xticks(rotation=25)
    # plt.show()
    plt.savefig(f'/home/petrov/dos_indent_app/static/plotnik{c+1}.png')
    plt.close()

def build_circle(labels,sizes):
        # Создаем данные для диаграммы
    # labels = ['A', 'B', 'C', 'D']
    # sizes = [15, 30, 45, 10]

    # Создаем круговую диаграмму
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    plt.tight_layout()

    # Сохраняем диаграмму в буфер
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Кодируем буфер в base64
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png).decode('utf-8')
    return graphic


def sort_traf(dump,host):
    enter_dump = []
    for i in dump:
        try:
                # if i.eth.src == mac:
                #     continue
            if i.ip.src == host:
                continue
            else:
                enter_dump.append(i)
        except Exception:
            continue
    print(len(enter_dump))
    return enter_dump

def get_time(a):
    # Инициализируем переменные min_time и max_time значением None
    min_time = 0
    max_time = 0

    # Проходим по всем пакетам в файле
    for packet in a:
        # Получаем значение поля "frame.time_epoch" для текущего пакета
        time_epoch = float(packet.frame_info.time_epoch)
        
        # Обновляем переменные min_time и max_time, если это необходимо
        if min_time == 0 or time_epoch < min_time:
            min_time = time_epoch
        if max_time == 0 or time_epoch > max_time:
            max_time = time_epoch

    # Вычисляем разницу между максимальным и минимальным временем в секундах
    time_diff = max_time - min_time
    print(time_diff)
    # Выводим результат
    print(f"Время между первым и последним пакетом в файле: {time_diff:.6f} секунд")
    return time_diff

def eq_koef(limit,dtime):
    lim_koef = limit/60
    cur_koef = limit/dtime
    r = lim_koef/cur_koef
    if r >= 0.85 and r <= 1:
        res = 1
    elif r>1:
        res = 2
    else:
        res = 0
    return res

def to_two_arr(original_list):
    even_list = original_list[::2] # четные индексы
    odd_list = original_list[1::2] # нечетные индексы
    return [even_list,odd_list]