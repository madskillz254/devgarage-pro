from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    posts = db.relationship('Post', backref='author', lazy=True)
    pass_secure = db.Column(db.String(255))

    # use the @property decorator to create a write only class property password
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        # generates a password hash.
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        # takes in a hash password and a password entered by a user and checks if the password matches to return a True or False response.
        return check_password_hash(self.pass_secure, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def save_review(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls, id):
        posts = Post.query.filter_by(id=id).all()
        return posts

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Quote:
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote



