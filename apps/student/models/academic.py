from config import db
from config import ma
from marshmallow_sqlalchemy import ModelSchema

from .student import Student


class AcademicInfo(db.Model):
    __bind_key__ = 'student'
    __tablename__ = 'academic_info'

    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.String(40),nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    standard = db.Column(db.String(3),nullable=False)
    section = db.Column(db.String(20),nullable=False)
    fee_type = db.Column(db.String(20),nullable=False)
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))

    def __init__(self, session, roll_no, standard, section, fee_type, student_id):
        self.session = session
        self.roll_no = roll_no
        self.standard = standard
        self.section = section
        self.fee_type = fee_type
        self.student_id = student_id


class AcademicSchema(ma.ModelSchema):
    class Meta:
        model = AcademicInfo


academic_schemas = AcademicSchema(many=True)

