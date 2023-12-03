from flask import Flask, flash, render_template, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from models import User, db
from werkzeug.security import generate_password_hash
from forms import  LoginForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
csrf = CSRFProtect(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)

@app.cli.command('create_db')
def create_db():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрированы!', 'success')
        return redirect(url_for('index'))
    return render_template('index.html', form=form)

@app.cli.command('read')
def read():
    #db.create_all()
    print(User.query.all())





