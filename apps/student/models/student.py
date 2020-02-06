import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from config import db
from config import ma
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship


class Student(db.Model):
    __bind_key__ = 'student'
    __tablename__ = 'student'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.String(20), unique=True, nullable=False)
    f_name = db.Column(db.String(100),nullable=False)
    m_name = db.Column(db.String(100),nullable=True)
    l_name = db.Column(db.String(100),nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    primary_contact = db.Column(db.String(10),unique=True,nullable=False)
    secondary_contact = db.Column(db.String(10),nullable=True)
    pwdhash = db.Column(db.String(200))
    address = relationship("StudentAddress", backref="student")
    personal = relationship("PersonalProfile", backref="student")
    academic = relationship("AcademicInfo",backref="student")
    # attendances = relationship("StudentAttendance",backref="student")
    is_student = db.Column(db.Boolean(),default=True)
    is_active = db.Column(db.Boolean(),default=False)
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow)

    def __init__(self, unique_id, f_name, m_name, l_name, gender, primary_contact, secondary_contact, email, password):
        self.unique_id = unique_id
        self.f_name = f_name
        self.m_name = m_name
        self.l_name = l_name
        self.gender = gender
        self.primary_contact = primary_contact
        self.secondary_contact = secondary_contact
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __repr__(self):
        return {'f_name':self.first_name, 'm_name':self.middle_name, 'last_name':self.l_name}


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "f_name", "m_name", "l_name", "gender", "primary_contact", "secondary_contact", "email","is_active", "created_at")


student_schemas = StudentSchema(many=True)
student_schema = StudentSchema()
