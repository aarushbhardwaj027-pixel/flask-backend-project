from flask import Flask,render_template,redirect,session
from auth.routes import auth_bp
from posts.routes import post_bp
from models import db

from flask_restx import Api, Resource, fields

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///data_insta.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = '0000'

app.register_blueprint(auth_bp , url_prefix = '/auth')
app.register_blueprint(post_bp ,url_prefix = '/post')

db.init_app(app)

@app.route("/")
def home():
    if 'user_id' in session:
        return redirect('/post')
    return render_template('index.html')

@app.route("/post")
def view():
    return render_template('post.html')

with app.app_context():
    db.create_all()

api = Api(app, version="1.0", title="Mini Insta API", description="Simple Instagram Clone API" ,doc="/docs")

ns = api.namespace('posts', description="Post operations")

post_model = api.model('Post', {
    'title': fields.String(required=True),
    'content': fields.String(required=True)
})



posts = []

@ns.route("/docs")
class PostList(Resource):

    def get(self):
        """Get all posts"""
        return posts

    @ns.expect(post_model)
    def post(self):
        """Create a new post"""
        data = api.payload

        post = {
            "title": data["title"],
            "content": data["content"]
        }

        posts.append(post)

        return {"message": "Post created", "post": post}

if __name__ == "__main__":
    app.run(debug=True)