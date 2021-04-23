from flask import *
from flask_mysqldb import MySQL
import os

UPLOAD_FOLDER = './upload'

smartIdScanner = Flask(__name__)

smartIdScanner.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

smartIdScanner.secret_key = 'Ha77rS99hA18'

smartIdScanner.config['MYSQL_HOST'] = 'remotemysql.com'
smartIdScanner.config['MYSQL_USER'] = 'd1lOwhi1PV'
smartIdScanner.config['MYSQL_PASSWORD'] = 'hqbOfjaWPc'
smartIdScanner.config['MYSQL_DB'] = 'd1lOwhi1PV'
mysql = MySQL(smartIdScanner)


@smartIdScanner.route('/')
def index():
    return render_template('index.html')


@smartIdScanner.route('/signup', methods=["GET","POST"])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO register VALUES (NULL, % s, % s, % s, % s)', (name, email, number, password))
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    else:
        msg = ''
    return render_template('signup.html', msg = msg)


@smartIdScanner.route('/login', methods=["GET","POST"])
def login():
    global userid
    msg = ''


    if request.method == 'POST' :
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM register WHERE email = % s AND password = % s', (email, password ))
        account = cursor.fetchone()
        print (account)
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            userid = account[0]
            session['email'] = account[1]

            return render_template('dashboard.html')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

@smartIdScanner.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('index.html')

@smartIdScanner.route('/upload', methods=["GET","POST"])
def upload():
    email = session['email']
    if request.method == 'POST':
        file = request.files['file']
        path = os.path.join(smartIdScanner.config['UPLOAD_FOLDER'], str(session['id']) + '__' + file.filename)
        file.save(path)
        msg = 'You have successfully uploaded !'
    return render_template('dashboard.html', msg = msg)

if __name__ == '__main__':
    smartIdScanner.run(debug=True)
