import sklearn 
import pickle
import flask
from flask import Flask, render_template, url_for, redirect, request, session
import sqlite3
# from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = '2w3w'
app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

model = pickle.load(open('heart_rd_model.sav', 'rb'))

@app.route('/', methods = ["POST","GET"])
def home_page():
    return render_template('about_index.html')

@app.route('/user_type', methods=["POST","GET"])
def user_type():
    return render_template('user_type.html')

@app.route('/user_login', methods=["POST","GET"])
def user_login():
    msg = 'Welcome back'
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']

            conn = sqlite3.connect("on_heart_db.db") 
            cur = conn.cursor()
            query1 = f"select * from customer where name = '{name}' and password = '{password}'"
            cur.execute(query1)

            if(len(cur.fetchall()) >= 1):
                conn.commit()
                session["user"] = request.form['name']
                return redirect(url_for("home_page"))
            else:
                msg = "u haven't login in before"
        except:
            msg = "fill properly"

    return render_template('user_login_index.html', msg=msg)

@app.route('/admin_login', methods=["POST","GET"])
def admin_login():
    msg = 'Admin Login'
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']

            conn = sqlite3.connect("on_heart_db.db") 
            cur = conn.cursor()
            query1 = f"select * from admin where name = '{name}' and password = '{password}'"
            cur.execute(query1)

            if(len(cur.fetchall()) >= 1):
                conn.commit()
                session["admin"] = request.form['name']
                return redirect(url_for("home_page"))
            else:
                msg = "u are not a Admin"
        except:
            msg = "fill properly"
    return render_template('admin_login_index.html', msg=msg)

@app.route('/sign_up', methods=["POST","GET"])
def sign_up():
    msg = 'Create your account'
    if request.method == "POST":
        try:
            name = request.form['name']
            password = request.form['password']
            city = request.form['city']
            conn = sqlite3.connect("on_heart_db.db") 
            cur = conn.cursor()
            query1 = f"INSERT INTO customer(name, password, city) VALUES ('{name}', '{password}', '{city}')"
            cur.execute(query1)
            conn.commit()
            msg = "Record successfully added"
            session["user"] = request.form['name']

            return redirect(url_for("home_page"))
        except:
            msg = "error in insert operation"

    return render_template('sign_up_index.html', msg=msg)

@app.route('/log_out', methods=["POST","GET"])
def log_out():
    session.pop("user", None)
    session.pop("admin", None)
    return redirect(url_for("home_page"))


@app.route('/check_up', methods=["POST","GET"])
def check_up():
    msg = 'Fill Details'
    if request.method == "POST":
        model_pred = []
        age = request.form.get('model_age')
        if str.isdigit(age) != True:
            return render_template('checkup_index.html', msg="Age must be integer")
        else:
            age = int(age)
            model_pred.append(age)

        gender = request.form.get('model_sex')
        if gender=="M":
            gender = 1
        else:
            gender = 0
        model_pred.append(gender)
        
        cp = request.form.get('model_cp')
        if cp == '':
            return render_template('checkup_index.html', msg="cp must be integer")
        else:
            cp = int(cp)
            model_pred.append(cp)

        trestbps = request.form.get('model_trestbps')
        if trestbps == '':
            return render_template('checkup_index.html', msg="trestbps must be integer")
        else:
            trestbps = int(trestbps)
            model_pred.append(trestbps)

        chol = request.form.get('model_chol')
        if chol == '':
            return render_template('checkup_index.html', msg="chol must be integer")
        else:
            chol = int(chol)
            model_pred.append(chol)

        fbs = request.form.get('model_fbs')
        if fbs == '':
            return render_template('checkup_index.html', msg="fbs must be integer")
        else:
            if int(fbs) > 120:
                fbs = 1
            else:
                fbs = 0
        model_pred.append(fbs)

        restecg = request.form.get('model_restecg')
        if restecg == '':
            return render_template('checkup_index.html', msg="restecg must be integer")
        else:
            restecg = int(restecg)
            model_pred.append(restecg)
            
        thalach = request.form.get('model_thalach')
        if thalach == '':
            return render_template('checkup_index.html', msg="thalach must be integer")
        else:
            thalach = int(thalach)
            model_pred.append(thalach)

        exang = request.form.get('model_exang')
        if exang == '':
            return render_template('checkup_index.html', msg="exang must be integer")
        else:
            exang = int(exang)
            model_pred.append(exang)

        oldpeak = request.form.get('model_oldpeak')
        if oldpeak == '':
            return render_template('checkup_index.html', msg="oldpeak must be integer")
        else:
            oldpeak = float(oldpeak)
            model_pred.append(oldpeak)

        slope = request.form.get('model_slope')
        if slope == '':
            return render_template('checkup_index.html', msg="slope must be integer")
        else:
            slope = int(slope)
            model_pred.append(slope)

        ca = request.form.get('model_ca')
        if ca == '':
            return render_template('checkup_index.html', msg="ca must be integer")
        else:
            ca = int(ca)
            model_pred.append(ca)

        thal = request.form.get('model_thal')
        if thal == '':
            return render_template('checkup_index.html', msg="thal must be integer")
        else:
            thal = int(thal)
            model_pred.append(thal)

        predicted = model.predict([model_pred])
        if predicted == [1]:
            predicted = 'you might be need help'
        else:
            predicted = 'you are Safe'
        return render_template('checkup_index.html', msg = predicted)

    return render_template('checkup_index.html', msg=msg)

@app.route('/doctor', methods=["POST","GET"])
def doctor():
    conn = sqlite3.connect("on_heart_db.db") 
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM doctor').fetchall()
    conn.close()
    return render_template('doctor_index.html', data=posts)

@app.route('/dashboard', methods=["POST","GET"])
def dashboard():
    return render_template('dashboard_index.html')

@app.route('/admin_data', methods=["POST","GET"])
def admin_data():
    conn = sqlite3.connect("on_heart_db.db") 
    conn.row_factory = sqlite3.Row
    posts = conn.execute('SELECT * FROM admin').fetchall()
    conn.close()
    return render_template('admin_data_index.html', data=posts)

# @app.route('/delete/<string:id>', methods=["POST","GET"])
# def delete_admin(id):
#     conn = sqlite3.connect("on_heart_db.db") 
#     cur = conn.cursor()
#     cur.execute(f"delete from admin where id= {id}")
#     conn.commit()
#     return redirect(url_for('admin_data'))

@app.route('/admin_delete/<int:admin_id>', methods=['POST'])

def delete_admin(admin_id):
    conn = sqlite3.connect("on_heart_db.db") 
    cur = conn.cursor()
    cur.execute(f"delete from admin where admin_id = {admin_id}")
    conn.commit()
    return redirect(url_for('admin_data'))


if __name__ == '__main__':
    app.run(debug=True)