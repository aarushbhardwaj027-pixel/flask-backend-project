from flask import render_template,redirect,Blueprint,request,session,url_for
from models import db,User,Post,Comments,Like

post_bp = Blueprint('post',__name__)

# _____________________________________ADD POST_________________________________


@post_bp.route('/add_post',methods = ['GET','POST'])
def add_post():
    if 'user_id' not in session:
        return redirect("/")

    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']

        u_id = session['user_id']


        post1 = Post(title = title ,content =content , user_id = u_id)

        db.session.add(post1)
        db.session.commit()

        return redirect('/post')

    return render_template('add_post.html')

# _____________________________________VIEW POST_________________________________

@post_bp.route('/view_posts')
def view():
    if 'user_id' in session:
        users = db.session.query(User).all()

        return render_template('view_all.html',users = users)
    else:
        return redirect('/')

# _____________________________________MY POST_________________________________

@post_bp.route('/my_posts')
def view_my():
    if 'user_id' in session:
        user = User.query.filter_by(id = session['user_id']).first()

        return render_template('view.html',user2 = user)
    else:
        return redirect('/')
    
# _____________________________________DEL MY POST_________________________________

    

@post_bp.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if post.user_id != session['user_id']:
        return redirect('/post')
    
    post = Post.query.get(id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/post")

# _____________________________________EDIT MY POST_________________________________


@post_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    if post.user_id != session['user_id']:
        return redirect('/post')
    post = Post.query.get(id)

    if request.method == "POST":
        post.title = request.form['title']
        post.content = request.form['content']

        db.session.commit()
        return redirect("/post/my_posts")

    return render_template("edit.html", post=post)

# _______________________________________________like______________________________________________

@post_bp.route("/like/<int:id>", methods=["POST"])
def like(id):

    if 'user_id' not in session:
        return redirect("/")

    count = Post.query.get(id)

    # 🔹 check if already liked
    existing = Like.query.filter_by(
        user_id=session['user_id'],
        post_id=id
    ).first()

    if existing:
        return redirect('/post/view_posts')   # already liked → do nothing

    # 🔹 if not liked → add like
    new_like = Like(user_id=session['user_id'], post_id=id)
    db.session.add(new_like)

    count.like += 1
    db.session.commit()

    return redirect('/post/view_posts')


# _______________________________________________dislike______________________________________________

@post_bp.route("/dislike/<int:id>", methods=["POST"])
def dislike(id):
    if 'user_id' not in session:
        return redirect("/")

    count = Post.query.get(id)

    existing = Like.query.filter_by(
        user_id=session['user_id'],
        post_id=id
    ).first()

    if existing:
        db.session.delete(existing)
        count.like -= 1
        db.session.commit()

    return redirect('/post/view_posts')

# _______________________________________________comment______________________________________________

@post_bp.route('/comment/<int:id>',methods = ['POST' , 'GET'])
def comment(id):
    if 'user_id' in session:
        if request.method == "POST":
            comment = request.form['comment']

            comment1 = Comments(comment = comment,post_id = id,user_id = session['user_id'])
            db.session.add(comment1)
            db.session.commit()

            print("comment added")

            return redirect('/post/view_posts')
        
        return render_template('comments.html')
