from flask import render_template,redirect,Blueprint,request,session
from models import db,User
from werkzeug.security import check_password_hash,generate_password_hash

auth_bp = Blueprint('auth',__name__)

# _____________________________________LOGIN_________________________________

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect("/post")   # or your feed/dashboard route

        return redirect("/")   # login failed

    return render_template("login.html")
    
# _____________________________________SIGNUP_________________________________

@auth_bp.route('/signup',methods = ["POST","GET"])
def signup():
        
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            session.pop('user_id',None)
            return redirect('/')
        else:

            encoded = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

            user1 = User(username=username, password=encoded)
            db.session.add(user1)
            db.session.commit()

            return redirect('/')

    return render_template('signup.html')


@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id',None)
        return redirect('/')
    else:
        return redirect('/')