from werkzeug.security import generate_password_hash , check_password_hash
import datetime
from config import db
from config import ma

class SuperAdmin(db.Model):

    __bind_key__ = 'super-admins'
    __tablename__ = 'super-admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pwdhash = db.Column(db.String(54))
    is_active = db.Column(db.Boolean(),default=True)
    is_staff = db.Column(db.Boolean(),default=True)
    is_admin = db.Column(db.Boolean(),default=True)
    is_super_admin = db.Column(db.Boolean(),default=True)
    created_on = db.Column(db.DateTime(),default=datetime.datetime.now())

    def __init__(self,username,name,email,password):
        self.username = username.lower()
        self.name = name.lower()
        self.email = email.lower()
        self.set_password(password)


    def set_password(self,password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.pwdhash,password)


class SuperAdminSChema(ma.Schema):
    class Meta:
        fields = ("id","username","email","is_active", "is_staff", "is_admin", "is_super_admin", "created_on")

super_admin_schema = SuperAdminSChema()
super_admins_schema = SuperAdminSChema(many=True)