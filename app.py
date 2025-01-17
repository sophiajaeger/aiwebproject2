from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from search import search # import search function from crawler.py 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__) # create instance of Flask app

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
# Enter a secret key
app.config["SECRET_KEY"] = "ENTER YOUR SECRET KEY"
# Initialize flask-sqlalchemy extension
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# create a class for saving user ID, name and password
class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url = db.Column(db.String(250), nullable=False)
    title = db.Column(db.String(250), nullable=False)
    teaser = db.Column(db.String(250), nullable=False)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route('/register', methods=["GET", "POST"])
def register():
  # create new user
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # check if username already exists
        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", 'error')
            return redirect(url_for("register"))
        
        # add user to database
        user = Users(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for("login"))
    # render register template if method is GET
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # search for user in the database
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        # check password 
        if user and user.password == password:
            login_user(user)
            flash('Login successful!', 'success')  # Success message
            return redirect(url_for('home'))
        flash('Invalid username or password. Please try again', 'error')
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/') # define home route ("/")
def home():
    return render_template('home.html')

@app.route('/search') # define the search rout ("/search")
def search_route():
    query = request.args.get('q')  # get search query from URL parameters
    if query:
        results, suggestions = search(query)  # pass to search function (crawler.py)
        return render_template('results.html', results=results, suggestions = suggestions)  # pas results to HTML tamplate
    return 'No query!'

@app.route('/bookmarks')
@login_required
def bookmarks():
    bookmarks = Bookmark.query.filter_by(user_id=current_user.id).all()
    return render_template('bookmarks.html', bookmarks=bookmarks)

@app.route('/bookmark', methods=['POST'])
@login_required  # Require user to be logged in
def bookmark():
    data = request.json
    url = data['url']
    title = data['title']
    teaser = data['teaser']

    # Check for existing bookmarks
    existing_bookmark = Bookmark.query.filter_by(user_id=current_user.id, url=url).first()
    if existing_bookmark:
        return jsonify({"error": "Bookmark already exists."}), 400  # Return an error if it exists
    bookmark = Bookmark(user_id=current_user.id, url=url, title=title, teaser=teaser)
    try:
        db.session.add(bookmark)
        db.session.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return error
    return '', 200

@app.route('/remove_bookmark', methods=['POST'])
@login_required
def remove_bookmark():
    url = request.form['url']
    bookmark = Bookmark.query.filter_by(user_id=current_user.id, url=url).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
    return redirect(url_for('bookmarks'))

def init_db():
    if not os.path.exists('db.sqlite'):
        with app.app_context():
            db.create_all()

# run the app in debug mode if this file is executed directly
if __name__ == '__main__':
    init_db()  # Initialize the database only if it does not exist
    app.run(debug=True)
