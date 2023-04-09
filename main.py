from flask import Flask, render_template, url_for, request, session
from werkzeug.utils import secure_filename
import sys
import os

app = Flask(__name__)    
app.secret_key = 'ebat_kakoy_secretniy_klu4'

@app.route('/', methods = ['get','post'])
def index():
    print(url_for('index'))

    if request.method == "POST":

        max_conn = request.form['max_conn']
        max_req_insec_oneip = request.form['max_req_insec_oneip']
        max_size_header = request.form['max_size_header']
        max_req_insec_allip = request.form['max_req_insec_allip']
        
        print(max_conn, max_req_insec_oneip, max_size_header, max_req_insec_allip)
        from new_ident import ident_dos

        a = ident_dos(int(max_conn), int(max_req_insec_oneip), int(max_size_header), int(max_req_insec_allip))

        return render_template(
                            'index.html',
                            r = a,
        )

    return render_template(
                           'index.html', 
                          )

#-----LOAD------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
