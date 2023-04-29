from flask import Flask, render_template, url_for, request, session
from werkzeug.utils import secure_filename
import sys
import os
from pyshark import FileCapture
from real_ident_ddos import current_file
from real_ident_ddos import add_dump
from real_ident_ddos import get_dname_from_db, get_file

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

        

        if file and current_file(file.filename):
            filename = secure_filename(file.filename)
            print('[*]main.py: filename - ' + str(filename))

            add_dump(str(filename)) # add dump name to database
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            dnsd = []
            tcpd = []
            icmpd = []
            arpd = []
            ssdpd = []
            ssld = []
            mdnsd = []
            datad = []
            nbns = []
            llmnrd =[]
            httpd = []
            vssmonitoringd = []
            data_text_linesd = []
            trash = []
            list_proto = ['DNS','TCP','ICMP','ARP','SSDP','SSL','MDNS','DATA','NBNS','LLMNR','HTTP','VSSMONITORING','DATA_TEXT_LINES','OTHER']

            all_proto = [dnsd, tcpd, icmpd, arpd, ssdpd, ssld, mdnsd, datad, nbns, llmnrd, httpd, vssmonitoringd, data_text_linesd, trash]

            dump = get_file(get_dname_from_db())
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
                if list_proto[8] == i.highest_layer:
                    all_proto[8].append(i)
                if list_proto[9] == i.highest_layer:
                    all_proto[9].append(i)
                if list_proto[10] == i.highest_layer:
                    all_proto[10].append(i)
                if list_proto[11] == i.highest_layer:
                    all_proto[11].append(i)
                if list_proto[12] == i.highest_layer:
                    all_proto[12].append(i)
                else:
                    all_proto[13].append(i)
            # print(all_proto)
            
            count_proto = []
            for i in all_proto:
                count_proto.append(len(i))
            print(list_proto)
            print(count_proto)    

            return render_template(
                'index.html',
                dlist = hlayer,
                d = dump,
                all_protocols = list_proto,
                count_protocols = count_proto,

            )
    
        if 'host' in request.form:
            host = request.form['host']
            port = request.form['port']
            max_conn = request.form['max_conn']
            max_req_insec_oneip = request.form['max_req_insec_oneip']
            max_size_header = request.form['max_size_header']
            max_req_insec_allip = request.form['max_req_insec_allip']

            print(max_conn, max_req_insec_oneip, max_size_header, max_req_insec_allip)
        # from new_ident import ident_dos

        # a = ident_dos(int(max_conn), int(max_req_insec_oneip), int(max_size_header), int(max_req_insec_allip), host, int(port))

        return render_template(
                            'index.html',
                            # r = c,
                            # host = host,
                            # port = port,
        )

    return render_template(
                           'index.html', 
                          )


@app.route('/about_us', methods = ['get','post'])
def about_us():
    print(url_for('about_us'))


    return render_template(
                           'about_us.html', 
                          )

#-----LOAD------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)