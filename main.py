from flask import Flask, render_template, url_for, request, session
from werkzeug.utils import secure_filename
import sys
import os

app = Flask(__name__)    
app.secret_key = 'ebat_kakoy_secretniy_klu4'

UPLOAD_FOLDER = 'dump_input/'
ALLOWED_EXTENSIONS = set(['pcap','pcapng'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))

    if request.method == "POST":
        file = request.files['file']
        from real_ident_ddos import current_file
        if file and current_file(file.filename):
            filename = secure_filename(file.filename)
            print('[*]main.py: filename - ' + str(filename))
            from real_ident_ddos import add_dump
            add_dump(str(filename)) # add dump name to database
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        from real_ident_ddos import cap
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