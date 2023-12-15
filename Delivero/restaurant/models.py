from wtforms.validators import Length
from restaurant import db, login_manager
from restaurant import bcrypt
from flask_login import UserMixin
from sqlalchemy.sql import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#USER TABLE
class User(db.Model, UserMixin):
   
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(length = 30), nullable = False, unique = True)
    fullname = db.Column(db.String(length = 30), nullable = False)
    address = db.Column(db.String(length = 50), nullable = False)
    phone_number = db.Column(db.Integer(), nullable = False)
    password_hash = db.Column(db.String(length = 60), nullable = False)

    tables = db.relationship('Table', backref = 'reserved_user', lazy = True) 
    items = db.relationship('Item', backref = 'ordered_user', lazy = True) 
    orders = db.relationship('Order', backref = 'order-id_user', lazy = True) 

    @property
    def password(self):
        return self.password
    
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        
    def assign_ownership(self, user):
        self.reservee = user.fullname 
        db.session.commit()


class Item(db.Model):
    
    item_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), nullable = False)
    description = db.Column(db.String(length = 50), nullable = False)
    price = db.Column(db.Integer(), nullable = False)
    source = db.Column(db.String(length = 30), nullable = False)
    
    orderer = db.Column(db.Integer(), db.ForeignKey('user.id')) 

    
    def assign_ownership(self, user):
        self.orderer = user.id 
        db.session.commit()

    def remove_ownership(self, user):
        self.orderer = None
        db.session.commit()


#ORDERS TABLE
class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(length = 30), db.ForeignKey('user.username'))
    address = db.Column(db.String(length = 30), nullable = False)
    order_items = db.Column(db.String(length = 300), nullable = False)
    datetime = db.Column(db.DateTime(timezone = True), server_default = func.now())


