from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'careerconnect'
app.config['MYSQL_DB'] = 'coder'
mysql = MySQL(app)

# Route for homepage
@app.route('/')
def index():
    return render_template('test.html')

# Route to handle image upload
@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # Get image file from the form
        image_file = request.files['file']
        # Read the image file
        image_data = image_file.read()
        # Open a connection to the MySQL database
        cur = mysql.connection.cursor()
        # Insert the image data into the table
        cur.execute("INSERT INTO image (print_image) VALUES (%s)", (image_data,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

# Route to display the uploaded image
@app.route('/display')
def display_image():
    # Open a connection to the MySQL database
    cur = mysql.connection.cursor()
    # Retrieve the image data from the table
    cur.execute("SELECT print_image FROM image ORDER BY id DESC LIMIT 1")
    image_data = cur.fetchone()[0]
    cur.close()
    return render_template('test.html', images=image_data)

if __name__ == '__main__':
    app.run(debug=True)
