from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, PasswordField

from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, login_required, logout_user
from resource.models import User, Work
from db import db
import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user


login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'data.sql') #found DB on root,in any os
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off flask track

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()


login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def index():
    return render_template('index.html', actives=True)


@app.route('/welcome')
@login_required
def welcome_user():
    return "WELCOME"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login_user', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email")).first()

        if user is not None and user.check_password(request.form.get("password")):
            login_user(user)
            flash('logged success')
            next = request.args.get('next')
            if next == None or not next[0] == '/':
                next = url_for('welcome_user')
            return redirect(url_for("works.add"))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')


###USERS###

@app.route('/add', methods=['GET', 'POST'])
def add_users():
    error = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        #!!! Verificar se ha registro igual
        # data = UserRegister.parser.parse_args()
        #
        # if UserModel.find_by_username(data['username']):
        #     return {"message": "name already taken"}, 400

        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=request.form.get("email")).first()
        login_user(user)

        return redirect(url_for('index'))

    return render_template("users/add_user.html", error=error)


@app.route('/del', methods=['GET', 'POST'])
def del_users():

    if request.method == "POST":
        _id = request.form.get("id")
        new_user = User.query.get(_id)
        db.session.delete(new_user)
        db.session.commit()

        return redirect(url_for('users.list_users'))
    return render_template("delete_user.html")


@app.route('/list')
def list_users():
    users = User.query.all()
    works = [1, 2, 3, 4]
    return render_template("users/list_users.html", all_users=users, all_works=works)


@app.route('/profile')
@login_required
def profile_users():
    works = Work.query.filter_by(user_id=current_user.id)
    alltime_work = Work.query.filter_by(user_id=current_user.id).count()
    return render_template("profile.html", alltime_work=alltime_work, name=current_user.name,
                           id_=current_user.id, working=current_user.working, all_works=works)

###WORKS###


@app.route('/add_work', methods=['GET', 'POST'])
@login_required
def add_works():
    works = Work.query.filter_by(user_id=current_user.id)
    time = datetime.now()
    try:
        id_ = current_user.id
        user_work = User.query.get(id_)
        work_final = Work.query.filter_by(user_id=current_user.id).order_by(Work.id.desc()).first()
        time = datetime.now() - work_final.time_init
        if work_final.time_init.strftime("%x") == datetime.now().strftime("%x") and not user_work.working:
            return render_template('index.html', actives=False)

    except:
        pass

    if request.method == "POST":
        id_ = current_user.id
        user_work = User.query.get(id_)

        if not user_work.working:
            user_work.working = True
            name = request.form.get("name")
            local = request.form.get("local")
            time_init = datetime.now()
            new_work = Work(name,local, id_, time_init)
            db.session.add(new_work)
        else:
            user_work.working = False
            work_final.time_final = datetime.now()
            db.session.add(work_final)
        db.session.add(user_work)
        db.session.commit()

        return redirect(url_for("works.add"))
    return render_template("add_work.html", time=time, works=works, active=current_user.working, name=current_user.name)


@app.route('/profile_work', methods=['GET', 'POST'])
@login_required
def profile_works():
    works = Work.query.filter_by(user_id=current_user.id)
    time = datetime.now()

    if False:
        return redirect(url_for("works.add"))
    return render_template("profile_work.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
