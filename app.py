from flask import Flask,render_template,redirect,session
from auth.routes import auth_bp
from posts.routes import post_bp
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///data_insta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = '0000'

app.register_blueprint(auth_bp , url_prefix = '/auth')
app.register_blueprint(post_bp ,url_prefix = '/post')

db.init_app(app)

@app.route("/")
def home():
    if 'user_id' not in session:
        return redirect('/auth/login')
    return render_template('index.html')

@app.route("/post")
def view():
    return render_template('post.html')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)