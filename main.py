from flask import Flask, render_template, url_for


app = Flask(__name__)

# В вашем Flask приложении
app.jinja_env.globals['static'] = lambda filename: url_for('static', filename = filename)

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



if __name__ == '__main__':
    app.run(debug = True, port = 5000)
