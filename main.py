from flask import Flask, render_template, url_for


app = Flask(__name__)
# В вашем Flask приложении
app.jinja_env.globals['static'] = lambda filename: url_for('static', filename = filename)


@app.route('/')
def home():
    """Главная страница"""
    return render_template('home.html', page='home')



if __name__ == '__main__':
    app.run(debug=True, port=5000)
