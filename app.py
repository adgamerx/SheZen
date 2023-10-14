from flask import Flask, send_file, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/safeRoute')
def safeRoute():
    return render_template('safeRoute.html')
if __name__ == '__main__':
    app.run(debug=True)
