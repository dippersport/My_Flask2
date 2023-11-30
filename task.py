from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        response = make_response(redirect(url_for('greet')))
        response.set_cookie('user_name', name)
        return response

@app.route('/hello')
def greet():
    user_name = request.cookies.get('user_name')
    if user_name:
        return render_template('welcome.html', user_name=user_name)
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_name')
    return response

if __name__ == '__main__':
    app.run(debug=True)
