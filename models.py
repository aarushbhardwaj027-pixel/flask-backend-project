from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
 
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)

    username = db.Column(db.String(200))
    password = db.Column(db.String(200))

    posts = db.relationship('Post', backref = 'author')
    comments = db.relationship('Comments', backref='user')

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(200))
    content = db.Column(db.String(500))
    like = db.Column(db.Integer, default = 0)
    dislike = db.Column(db.Integer, default = 0)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    comments = db.relationship('Comments', backref='post')


class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key = True)

    comment = db.Column(db.String(500))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))