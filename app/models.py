from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class UserLogin(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'user_login'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80),nullable=False)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120),nullable=False)
    date = db.Column(db.DateTime, default = datetime.utcnow)
    password= db.Column(db.String(255))


    def __init__(self, first_name, last_name, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)

class User_Profile(db.Model):

    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.TEXT,nullable=True)
    alergies = db.Column(db.TEXT,nullable=True)
    fav_categories = db.Column(db.TEXT,nullable=True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)


    def __init__(self, id , ingredients, alergies, fav_categories, date_added):
        self.id = id
        self.ingredients = ingredients
        self.alergies = alergies
        self.fav_categories = fav_categories
        self.date_added = date_added



