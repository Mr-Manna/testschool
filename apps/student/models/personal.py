import datetime
from config import db
from config import ma
from marshmallow_sqlalchemy import ModelSchema

from .student import Student


class StudentAddress(db.Model):
    __bind_key__ = 'student'
    __tablename__ = 'student_address'

    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.String(10),nullable=False)
    location = db.Column(db.String(300),unique=True,nullable=False)
    pincode = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def __init__(self, address_type, location, pincode, city, state, student_id):
        self.address_type = address_type
        self.location = location
        self.pincode = pincode
        self.city = city
        self.state = state
        self.student_id = student_id


class StudentAddressSchema(ModelSchema):
    class Meta:
        fields = ("id", "address_type", "location", "pincode", "city", "state" )


student_address_schema = StudentAddressSchema()
student_addresses_schema = StudentAddressSchema(many=True)


class StudentAvatar(db.Model):
    __bind_key__ = 'student'
    __tablename__ = 'student_avatar'

    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))
    avatar = db.Column(db.LargeBinary)


class StudentAvatarSchema(ma.Schema):
    class Meta:
        fields = ("id", "student_id", "avatar" )


student_avatar_schema = StudentAvatarSchema()
students_avatar_schema = StudentAvatarSchema(many=True)


class PersonalProfile(db.Model):
    __bind_key__ = 'student'
    __tablename__ = 'personal_profile'
    id = db.Column(db.Integer,primary_key=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))
    dob = db.Column(db.String(70), nullable=False)
    blood_group = db.Column(db.String(70), nullable=False)
    father_name = db.Column(db.String(70), nullable=False)
    mother_name = db.Column(db.String(70), nullable=False)
    father_profession = db.Column(db.String(70), nullable=False)
    mother_profession = db.Column(db.String(70), nullable=False)


class PersonalSchema(ma.ModelSchema):
    class Meta:
        model: PersonalProfile


student_personal_profile = PersonalSchema()
students_personal_profile = PersonalSchema(many=True)