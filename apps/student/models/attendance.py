from config import db
from config import ma
import datetime


class StudentAttendance(db.Model):

    __bind_key__ = "student"
    __tablename__ = "student_attendance"

    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Date(), default=datetime.date)
    time = db.Column(db.Time(), default=datetime.time)
    presents = db.Column(db.Integer(), nullable=True)
    absents = db.Column(db.Integer(), nullable=True)
    student_id = db.Column(db.Integer(), db.ForeignKey('student.id'))

    def __init__(self, date, time, presents, absents, student_id):
        self.date = date
        self.time = time
        self.presents = presents
        self.absents = absents
        self.student_id = student_id





