from flask import Flask,render_template,request,redirect,flash,url_for
from models import Users,Posts
from flask_login import LoginManager,login_user,logout_user,current_user
from flask_bcrypt import Bcrypt

def register_routes(app,db,bcrypt):

    @app.route("/",methods=["GET","POST"])
    def index():
        users=Users.query.all()
        return render_template("index.html",current_user=current_user)
    
    @app.route("/create",methods=["GET","POST"])
    def create():
        if request.method=="GET":
            return render_template("create.html")
        elif request.method=="POST":

            title=request.form.get('title')
            content=request.form.get('content')


            post=Posts(title=title,content=content,user_id=current_user.uid)

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('dashboard'))

    @app.route("/dashboard")
    def dashboard():
        posts = Posts.query.filter_by(user_id=current_user.uid).all()
        return render_template("LoggedInUser.html", posts=posts)


    @app.route("/delete/<int:post_id>")
    def delete(post_id):
        
        post = Posts.query.get_or_404(post_id)  # Fetch the post by id, 404 if not found
        if post.user_id != current_user.uid:  # Check if the current user is the author of the post
            flash('You are not authorized to delete this post.', 'danger')
            return redirect(url_for('dashboard'))

        db.session.delete(post)  # Delete the post
        db.session.commit()  # Commit changes to the database
        flash('The post has been deleted successfully.', 'success')
        return redirect(url_for('dashboard'))



    @app.route("/edit/<int:post_id>", methods=["GET", "POST"])
    def edit(post_id):
        post = Posts.query.get_or_404(post_id)  # Fetch post by ID or return 404 if not found
        
        if post.user_id != current_user.uid:
            flash("You are not authorized to edit this post!")
            return redirect(url_for('dashboard'))

        if request.method == "POST":
            post.title = request.form.get("title")
            post.content = request.form.get("content")
            db.session.commit()
            flash("Post updated successfully!")
            return redirect(url_for('dashboard'))
        return render_template("edit.html", post=post)

    @app.route("/all")
    def allposts():

        posts=Posts.query.all()
        print(posts)
        return render_template("allPosts.html",posts=posts)
    @app.route("/login",methods=["GET","POST"])
    def login():
        if request.method=="GET":
            return render_template("login.html")
        elif request.method=="POST":
            username=request.form.get('username')
            password=request.form.get('password')


            user=Users.query.filter(Users.username==username).first()
            if user and bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                return redirect(url_for('signup'))
            
    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for('index'))


    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "GET":
            return render_template("signup.html")
        
        elif request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password=bcrypt.generate_password_hash(password).decode('utf-8')
            existing_user = Users.query.filter_by(username=username).first()

            if existing_user:
                flash("Username already taken. Please Login")
                return redirect(url_for('login'))
            user = Users(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))
