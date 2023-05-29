filename = 'dump_input/petr.pcapng'
from pyshark import FileCapture
a = FileCapture(str(filename))
print(a)

def get_count_ip(proto,arr):
    c_ip = []
    final_dict = {}
    unique = []
    for j in proto:
        for i in arr:
            # print(i.highest_layer)
            if i.highest_layer == j:
                c_ip.append(i.ip.src)
        
        for i in c_ip:
            if i in unique:
                continue
            else:
                if '127.0.0' in i:
                    continue
                else:
                    unique.append(i)
        # print(unique)
        final_dict[f"{j}"]=unique
        unique = []
        c_ip = []

    return final_dict

# print(get_count_ip(['DNS','SSL','TCP'],a))
# {'DNS': ['192.168.49.139', '192.168.49.2'], 'SSL': ['192.168.49.139', '198.16.76.27', '78.47.62.131', '198.16.66.125'], 'TCP': ['192.168.49.139']}