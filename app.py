from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate("data.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://lenden-37532-default-rtdb.firebaseio.com/'
})

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/sing', methods=['GET', 'POST'])
def si():
    if request.method == 'POST':
        user_name = request.form['name']
        user_number = request.form['phone']
        user_pass = request.form['pass']

        ref = db.reference(f'Lenden app/users/{user_name}')
        ref.update({
            'name': user_name.lower(),
            'number': user_number,
            'password': user_pass
        })
    return render_template('sing_page.html')

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        user_name = request.form['name']
        user_pass = request.form['pass']

        ref = db.reference(f'Lenden app/users/{user_name}')
        data = ref.get()

        if data and data['name'] == user_name.lower() and data['password'] == user_pass:
            print("Redirecting to /user with ms=yes")  # Debug print
            return redirect(url_for('user', ms="User Panel",name=data["name"]))
        else:
            print("Login failed or data not matched")

    return render_template('log_page.html')

@app.route('/user')
def user():
    msg = request.args.get('ms')
    user_name = request.args.get('name')
    print(f"Received query param: ms = {msg}")  # Debug print
    return render_template('user.html', message=msg,name=user_name)

if __name__ == '__main__':
    app.run(debug=True)
