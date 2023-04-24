from flask import Flask, render_template, redirect, make_response, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.user import LoginForm, RegisterForm
from forms.teacher import LoginFormTeach, RegisterFormTeach
from forms.projects import ProjectsForm
from data.users import User
from data.teachers import Teacher
from data.projects import Projects
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/projects.db")
db_sess = db_session.create_session()

login_manager = LoginManager()
login_manager.init_app(app)
#---------------То что выводится после входа-------------------
@app.route("/")
@app.route("/all_projects")
def index():
    if current_user.is_authenticated:
        projects = db_sess.query(Projects).filter((Projects.user == current_user) | (Projects.is_private != True))
    else:
        projects = db_sess.query(Projects).filter(Projects.is_private != True)
    return render_template("index.html", projects=projects)

@app.route("/my_projects")
def index_2():
    if current_user.is_authenticated:
        projects = db_sess.query(Projects).filter((Projects.user == current_user) | (Projects.is_private != True))
    else:
        projects = db_sess.query(Projects).filter(Projects.is_private != True)
    return render_template("index-2.html", projects=projects)

@app.route("/account")
def account():
    projects = db_sess.query(User)
    return render_template("account.html", projects=projects)

#-------для учителя------
@app.route("/all_projects_teach")
def all_index_teach():
    if current_user.is_authenticated:
        projects = db_sess.query(Projects).filter((Projects.user == current_user) | (Projects.is_private != True))
    else:
        projects = db_sess.query(Projects).filter(Projects.is_private != True)
    return render_template("all-index-teach.html", projects=projects)

@app.route("/my_projects_teach")
def my_index_teach():
    if current_user.is_authenticated:
        projects = db_sess.query(Projects).filter((Projects.user == current_user) | (Projects.is_private != True))
    else:
        projects = db_sess.query(Projects).filter(Projects.is_private != True)
    return render_template("my-index-teach.html", projects=projects)

@app.route("/account_teach")
def account_teach():
    projects = db_sess.query(Teacher)
    return render_template("account-teach.html", projects=projects)
#----------------------------------------------------------------
#---------------Два класса отвечающих за вход--------------------
@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/login_teach', methods=['GET', 'POST'])
def login_teach():
    form = LoginFormTeach()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        teacher = db_sess.query(Teacher).filter(Teacher.email == form.email.data).first()
        if teacher and teacher.check_password(form.password.data):
            login_user(teacher, remember=form.remember_me.data)
            return redirect("/all_projects_teach")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)
#----------------------------------------------------------------
#---------------Класс отвечающий за регистрацию------------------
@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/register_teach', methods=['GET', 'POST'])
def reqister_teach():
    form = RegisterFormTeach()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register-teach.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register-teach.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        a = ''
        if form.mathematics.data:
            a += 'Математика, '
        if form.physics.data:
            a += 'Физика, '
        if form.informatics.data:
            a += 'Информатика'
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess = db_session.create_session()
        if db_sess.query(Teacher).filter(Teacher.email == form.email.data).first():
            return render_template('register-teach.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        
        teacher = Teacher(
            name=form.name.data,
            email=form.email.data,
            lessons=f'{a}',
            about=form.about.data
        )
        teacher.set_password(form.password.data)
        db_sess.add(teacher)
        db_sess.commit()
        return redirect('/login')
    return render_template('register-teach.html', title='Регистрация', form=form)
#----------------------------------------------------------------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/projects',  methods=['GET', 'POST'])
@login_required
def add_projects():
    form = ProjectsForm()
    if form.validate_on_submit():
        a = form.teachername.data
        print(a)
        if not db_sess.query(Teacher).filter(Teacher.name == a).first():
            return render_template('projects.html', title='Добавление проекта', 
                           form=form, message='Такого учителя не существует')
        projects = Projects()
        projects.title = form.title.data
        projects.content = form.content.data
        projects.teachername = a
        projects.is_private = form.is_private.data
        current_user.projects.append(projects)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/my_projects')
    return render_template('projects.html', title='Добавление проекта', 
                           form=form)

@app.route('/projects/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_projects(id):
    form = ProjectsForm()
    if request.method == "GET":
        projects = db_sess.query(Projects).filter(Projects.id == id,
                                          Projects.user == current_user
                                          ).first()
        if projects:
            form.title.data = projects.title
            form.content.data = projects.content
            projects.teachername = form.teachername.data
            form.is_private.data = projects.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        projects = db_sess.query(Projects).filter(Projects.id == id,
                                          Projects.user == current_user
                                          ).first()
        if projects:
            projects.title = form.title.data
            projects.content = form.content.data
            projects.teachername = form.teachername.data
            projects.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('projects.html',
                           title='Редактирование новости',
                           form=form
                           )

@app.route('/projects_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def projects_delete(id):
    projects = db_sess.query(Projects).filter(Projects.id == id,
                                      Projects.user == current_user
                                      ).first()
    if projects:
        db_sess.delete(projects)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

