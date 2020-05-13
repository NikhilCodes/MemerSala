from flask import Flask, redirect, request, render_template, url_for, send_from_directory
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
from passlib.hash import sha512_crypt
from random import randint
from time import asctime
import webbrowser
import pickle

app = Flask(__name__)
app.secret_key = "nikhilisalpha966313022001"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

dbfile = open("db/db.pickle", "rb")
database = pickle.load(dbfile)
dbfile.close()


class User(UserMixin):
    def __init__(self, id):
        self.id = id
    
    def repr(self):
        return self.id


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    content = []
    with open('db/content-log.log') as f:
        data = f.read().rstrip('\n')
        if data == '':
            content = None
        else:
            for line in data.split('\n'):
                content.append(line.split("???:???"))

    return render_template("home.html", uname=current_user.get_id().lower(), contents=content)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        if request.form['username'].lower() in database.keys() and sha512_crypt.verify(request.form['password'], database[request.form['username'].lower()]):
            login_user(User(request.form['username']))
            return redirect(url_for('home'))
        else:
            error = "Invalid, Credentials!"

    return render_template("login.html", error=error)


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == "POST":
        if ' ' in request.form['username']:
            error = "Username cannot contain spaces!"
        elif request.form['password0'] != request.form['password1']:
            error = "Passwords must Match!"
        elif request.form['username'] in database.keys():
            error = "User already Exists!"
        else:
            user_name = request.form['username'].lower()
            password = sha512_crypt.hash(request.form['password0'])
            database[user_name] = password
            with open('db/db.pickle', 'wb') as f:
                pickle.dump(database, f)

            login_user(User(request.form['username']))
            return redirect(url_for('home'))

    return render_template("signup.html", error=error)


@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@login_manager.user_loader
def load_user(userid):
    return User(userid)


@app.route('/chat-history/<path:path>', methods=['GET', 'POST'])
def send_log(path):
    return send_from_directory('db', 'chat-log.log')


@app.route("/post-chat/", methods=["GET", "POST"])
def post_chat():
    if request.form['chat_input'] != '':
        with open('db/chat-log.log', 'r') as f:
            prev_data = f.read()

        with open('db/chat-log.log', 'w') as f:
            f.write("""<strong>{}</strong>: {}\n<br>\n""".format(current_user.get_id().lower(),
                                                                 request.form['chat_input'])
                    + prev_data)

    return render_template("chat-textbox.html")


@app.route('/uploader/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['meme-file']
        file_name = secure_filename(f.filename)
        f.save("db/contents/" + file_name)
        with open("db/content-log.log", 'r') as f:
            prev_data = f.read()

        with open("db/content-log.log", 'w') as f:
            f.write(file_name+"???:???"+asctime()+"???:???"+current_user.get_id()+"???:???"+request.form["caption-text"]+"\n"+prev_data)

        return redirect(url_for('home'))


@app.route('/scripts/<path:path>', methods=['GET', 'POST'])
def send_js(path):
    return send_from_directory('scripts', path)


@app.route('/templates/<path:path>', methods=['GET', 'POST'])
def send_html(path):
    return send_from_directory('templates', path)


@app.route('/content/<path:path>', methods=['GET', 'POST'])
def send_content(path):
    return send_from_directory('db/contents', path)


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host='0.0.0.0', port=8000)
