from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
import base64
import datetime
import requests
app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'careerconnect'
app.config['MYSQL_DB'] = 'coder'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add_cloth')
def index():
    return render_template('addcloth.html')

@app.route('/add', methods=['POST'])
def add_cloth():
    if request.method == 'POST':
        cloth_type = request.form['cloth_type']
        file = request.files['file']
        response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': (file.filename, file.stream, file.mimetype)},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'E36TLzJzrCaeqjtaG4Pn6eKg'},
    )

    if response.status_code == requests.codes.ok:
        print("helloo")
        file = response.content
        if file and cloth_type:
            filename = file.filename
            cur = mysql.connection.cursor()
            if cloth_type == 'top':
                cur.execute("INSERT INTO top (top_img) VALUES (%s)", (filename,))
            elif cloth_type == 'bottom':
                cur.execute("INSERT INTO bottom (bottom_img) VALUES (%s)", (filename,))
            elif cloth_type == 'shoes':
                cur.execute("INSERT INTO shoes (shoes_img) VALUES (%s)", (filename,))
            mysql.connection.commit()
            cur.close()
    return redirect(url_for('index'))

@app.route('/view_clothes')
def view_clothes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM top")
    tops = cur.fetchall()
    cur.execute("SELECT * FROM bottom")
    bottoms = cur.fetchall()
    cur.execute("SELECT * FROM shoes")
    shoes = cur.fetchall()
    cur.close()

    tops_with_images = []
    bottoms_with_images = []
    shoes_with_images = []

    for top in tops:
        top_with_image = (top[0], base64.b64encode(top[1]).decode('utf-8'))
        tops_with_images.append(top_with_image)

    for bottom in bottoms:
        bottom_with_image = (bottom[0], base64.b64encode(bottom[1]).decode('utf-8'))
        bottoms_with_images.append(bottom_with_image)

    for shoe in shoes:
        shoe_with_image = (shoe[0], base64.b64encode(shoe[1]).decode('utf-8'))
        shoes_with_images.append(shoe_with_image)
    return render_template('viewcloth.html', tops=tops_with_images, bottoms=bottoms_with_images, shoes=shoes_with_images)

@app.route('/delete_cloth/<string:cloth_type>/<int:cloth_id>', methods=['POST'])
def delete_cloth(cloth_type, cloth_id):
    cur = mysql.connection.cursor()
    if cloth_type == 'top':
        cur.execute("DELETE FROM top WHERE id = %s", (cloth_id,))
    elif cloth_type == 'bottom':
        cur.execute("DELETE FROM bottom WHERE id = %s", (cloth_id,))
    elif cloth_type == 'shoes':
        cur.execute("DELETE FROM shoes WHERE id = %s", (cloth_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view_clothes'))



@app.route('/upload1', methods=['POST'])
def upload1():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': (file.filename, file.stream, file.mimetype)},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'E36TLzJzrCaeqjtaG4Pn6eKg'},
    )

    if response.status_code == requests.codes.ok:
        img_data=response.content

    cursor = mysql.connection.cursor()

    cursor.execute("INSERT INTO top (top_img) VALUES (%s)", (img_data,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/upload2', methods=['POST'])
def upload2():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']
    if file.filename == '':
        return redirect('/')
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': (file.filename, file.stream, file.mimetype)},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'E36TLzJzrCaeqjtaG4Pn6eKg'},
    )

    if response.status_code == requests.codes.ok:
        img_data=response.content

    cursor = mysql.connection.cursor()

    cursor.execute("INSERT INTO bottom (bottom_img) VALUES (%s)", (img_data,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/upload3', methods=['POST'])
def upload3():
    if 'file' not in request.files:
        return redirect('/')
    
    file = request.files['file']

    if file.filename == '':
        return redirect('/')

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': (file.filename, file.stream, file.mimetype)},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'E36TLzJzrCaeqjtaG4Pn6eKg'},
    )

    if response.status_code == requests.codes.ok:
        img_data=response.content


    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO shoes (shoes_img) VALUES (%s)", (img_data,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/choose_dress')
def choose_dress():
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM top ORDER BY RAND() LIMIT 1")
    top = cur.fetchone()[1]
    top=base64.b64encode(top).decode('utf-8')
    cur.execute("SELECT * FROM bottom ORDER BY RAND() LIMIT 1")
    bottom = cur.fetchone()[1]
    bottom=base64.b64encode(bottom).decode('utf-8')
    cur.execute("SELECT * FROM shoes ORDER BY RAND() LIMIT 1")
    shoes= cur.fetchone()[1]

    shoes=base64.b64encode(shoes).decode('utf-8')
    print(shoes)
    cur.close()

    return render_template('choose_dress.html', top=top, bottom=bottom, shoes=shoes,date=datetime.datetime.now().strftime('%d-%m-%Y'))

@app.route('/reroll')
def reroll():
    return choose_dress()

@app.route('/home')
def home1():
    return redirect(url_for("home"))


@app.route('/lock_wardrobe')
def lock():
    return render_template( 'lock_wardrobe.html')


if __name__ == '__main__':
    app.run(debug=True)
