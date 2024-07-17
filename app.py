# Pip install waitress
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN
import os  # If you need os operations


app = Flask(__name__)



app.url_map.strict_slashes = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'Students'

# mysql = MySQL(app)

@app.route("/")

@app.route('/home', methods=['GET', 'POST'])
def home():
    title = 'Home'
    if request.method == 'POST' and 'datafile' in request.files:
        file = request.files['datafile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            df = pd.read_csv(file) #Assuming the file is a CSV

            hist, edges = np.histogram(df, bins = 50) #adjust based on ur data's column
            p = figure(title="Data Histogram", background_fill_color= "#fafafa" , width=400, height=400,)
            p.quad(top=hist, bottom = 0, left = edges[:-1], right = edges[1:], fill_color = "navy", line_color = "white")

            #generate the bokeh components to embed in the HTML
            script, div = components(p)
            cdn_js = CDN.js_files[0]# get the CDN JS files for Bokeh
            return render_template('index.html', script = script, div=div, cdn_js = cdn_js )

    # defualt Render template with components
    return render_template('index.html')



@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        userdetails = request.form
        fname = userdetails['fname']
        # cur = mysql.connection.cursor()
        # cur.execute("INSERT INTO student(idnum,name) VALUES(%i,%s)",(54252,'Testing1'))
        # mysql.connection.commit()
        # cur.close()
        # return "{name}"
    return render_template('contact.html')



from flask import Flask, request, jsonify
from astropy.io.votable import parse_single_table

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['datafile']
    table = parse_single_table(file.stream)
    data = table.array
    result = data.tolist()  # Assuming the data can be directly converted to a list
    return jsonify(result)


@app.route('/user_manual', methods=['GET'])
def user_manual():
    return render_template('user_manual.html')



if __name__ == '__main__':
    #serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True)
