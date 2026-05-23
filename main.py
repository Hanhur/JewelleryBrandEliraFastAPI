from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elira.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'
db = SQLAlchemy(app)

# В вашем Flask приложении
app.jinja_env.globals['static'] = lambda filename: url_for('static', filename = filename)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(100), nullable = True)
    last_name = db.Column(db.String(100), nullable = True)
    phone = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(300), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)


# Создаем таблицы в базе данных
with app.app_context():
    db.create_all()
    print("База данных и таблицы созданы!")

@app.route('/')
def home():
    """Главная страница"""
    return render_template('home.html', page = 'home')

@app.route('/about')
def about():
    """Страница о нас"""
    return render_template('about.html', page = 'about')

@app.route('/coupons')
def coupons():
    """Страница Coupons"""
    return render_template('coupons.html', page = 'coupons')

@app.route('/stores')
def stores():
    """Страница Stores"""
    return render_template('stores.html', page = 'stores')

@app.route('/connect')
def connect():
    """Страница Connect"""
    return render_template('connect.html', page = 'connect')


@app.route('/sign')
def sign():
    """Страница Sign In"""
    return render_template('sign.html', page = 'sign')

@app.route("/posts")
def posts():
    """Страница со всеми сообщениями"""
    posts = Post.query.order_by(Post.date.desc()).all()  # Сортируем по дате (новые сверху)
    return render_template("posts.html", posts = posts)


@app.route('/contact', methods = ["POST", "GET"])
def contact():
    """Страница Contact с формой отправки сообщения"""
    if request.method == "POST":
        try:
            # Получаем данные из формы
            first_name = request.form.get('first_name', '').strip()
            last_name = request.form.get('last_name', '').strip()
            phone = request.form.get('number', '').strip()
            email = request.form.get('email', '').strip()
            text = request.form.get('text', '').strip()
            
            # Проверяем, что обязательные поля заполнены
            if not phone or not email or not text:
                flash('Пожалуйста, заполните все обязательные поля (Phone, Email, Message)!', 'error')
                return redirect('/contact')
            
            # Создаем новое сообщение
            post = Post(
                first_name = first_name,
                last_name = last_name,
                phone = phone,
                email = email,
                text = text
            )
            
            # Сохраняем в базу данных
            db.session.add(post)
            db.session.commit()
            
            flash('Сообщение успешно отправлено!', 'success')
            return redirect("/posts")
            
        except Exception as e:
            db.session.rollback()
            flash(f'При добавлении сообщения произошла ошибка: {str(e)}', 'error')
            return redirect('/contact')
    
    return render_template('contact.html', page = 'contact')


if __name__ == '__main__':
    app.run(debug = True, port = 5000)
