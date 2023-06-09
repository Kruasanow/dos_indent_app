from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
import sys
import os
from real_ident_ddos import current_file
from real_ident_ddos import add_dump, get_dname_from_db, get_file, build_circle, sort_traf, get_time, eq_koef, to_two_arr

app = Flask(__name__)    
app.secret_key = 'ebat_kakoy_secretniy_klu4'

UPLOAD_FOLDER = 'dump_input/'
ALLOWED_EXTENSIONS = set(['pcap','pcapng'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def current_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))

    if request.method == "POST":
        file = request.files['file']

        if file and current_file(file.filename) and 'limit' in request.form and 'host' in request.form:
            filename = secure_filename(file.filename)
            print('[*]main.py: filename - ' + str(filename))

            add_dump(str(filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            dnsd = []
            tcpd = []
            icmpd = []
            arpd = []
            ssld = []
            httpd = []
            vssmonitoringd = []
            data_text_linesd = []
            trash = []

            list_proto = ['DNS','TCP','ICMP','ARP','SSL','HTTP','VSSmon','DATA','Unexplored']
            from new_test import get_count_ip
            # res_get_ip = get_count_ip(list_proto)

            all_proto = [dnsd, tcpd, icmpd, arpd, ssld, httpd, vssmonitoringd, data_text_linesd, trash]

            host = request.form['host']
            try:
                limit = int(request.form['limit'])
            except Exception:
                limit = 20

            dumpb = get_file(get_dname_from_db())
            # print('start dump - '+str(len(dumpb)))
            dump = sort_traf(dumpb,host)
            # print('finish dump - '+str(len(dump)))
            hlayer = []
            for i in dump:
                hlayer.append(i.highest_layer)
                if list_proto[0] == i.highest_layer:
                    all_proto[0].append(i)
                if list_proto[1] == i.highest_layer:
                    all_proto[1].append(i)
                if list_proto[2] == i.highest_layer:
                    all_proto[2].append(i)
                if list_proto[3] == i.highest_layer:
                    all_proto[3].append(i)
                if list_proto[4] == i.highest_layer:
                    all_proto[4].append(i)
                if list_proto[5] == i.highest_layer:
                    all_proto[5].append(i)
                if list_proto[6] == i.highest_layer:
                    all_proto[6].append(i)
                if list_proto[7] == i.highest_layer:
                    all_proto[7].append(i)
                else:
                    all_proto[8].append(i)
            
            count_proto = []
            for i in all_proto:
                count_proto.append(len(i))
            print('########################')
            print(list_proto)
            print(count_proto)    

            ddos_id = []
            ddos_mb_id = []
            ddos_no = []
            for index in all_proto:
                tm = get_time(index)
                try:
                    res = eq_koef(limit,tm)
                except Exception:
                    continue
                if res == 2:
                    ddos_id.append(index[0].highest_layer)
                    ddos_id.append(tm)
                    ddos_id.append(list(get_count_ip([f'{index[0].highest_layer}'],dump).values()))
                if res == 1:
                    ddos_mb_id.append(index[0].highest_layer)
                    ddos_mb_id.append(tm)
                    ddos_mb_id.append(list(get_count_ip([f'{index[0].highest_layer}'],dump).values()))
                if res == 0:
                    ddos_no.append(index[0].highest_layer)
                    ddos_no.append(tm)



            warn_arr = to_two_arr(ddos_id)
            alert_arr = to_two_arr(ddos_mb_id)
            # warn_arr = to_two_arr(ddos_id)
            # alert_arr = to_two_arr(ddos_mb_id)
            print('1########################')

            circle = []
            # print(list_proto)
            # print(count_proto)  
            # print(sum(count_proto))
            print('########################')
            for i,l in zip(count_proto,list_proto):
                ii = [i,sum(count_proto)]
                print(ii)
                ll = [l,'Др.Прот.']
                print(ll)
                circle.append(build_circle(ll,ii))


            from real_ident_ddos import get_time_grath
            p = 0
            for ind in list_proto:
                # print(ind)
                get_time_grath(dump,ind,p)
                p+=1
            ####
            return render_template(
                'index.html',
                dlist = hlayer,
                d = dump,
                all_protocols = list_proto,
                count_protocols = count_proto,
                circ = circle,
                warn0 = warn_arr[0],
                warn1 = warn_arr[1],
                warn3 = warn_arr[2],
                alert1 = alert_arr[0],
                alert2 = alert_arr[1],
                alert3 = alert_arr[2],
            )
        

    return render_template(
                           'index.html', 
                          )


@app.route('/about_us', methods = ['get','post'])
def about_us():
    print(url_for('about_us'))
    
    import subprocess

    def add_iptables_rule(rule):
        command = ['iptables', '-A', 'INPUT'] + rule.split()
        subprocess.run(command, check=True)

    def block_ip(ip):
        rule = f'-s {ip} -j DROP'
        add_iptables_rule(rule)
        a = subprocess.check_output(['iptables-save'])
        return a

    if request.method == "POST":   

        if 'ipb' in request.form:
            ipb = request.form['ipb']
            b = block_ip(str(ipb))
            return render_template(
                    'about_us.html',
                    b = b
                    )
        return render_template(
                           'about_us.html', 
                          )
    return render_template(
                           'about_us.html', 
                          )

#-----LOAD------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
