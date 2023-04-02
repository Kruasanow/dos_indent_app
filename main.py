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
        file = request.files['file']

    return render_template(
                           'index.html', 
                          )

#-----LOAD------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
