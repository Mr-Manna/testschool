from flask import request, session,make_response
from flask import jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity,create_refresh_token
)
from flask_mail import Message
import smtplib

from config import db
from config import mail

# Imported Database
from ..models.student import Student
from ..models.student import student_schema,student_schemas

# smtpObj = smtplib.SMTP("smtp.mailtrap.io", 2525)
# smtpObj.login("046c0d3e002858", "4424339fab32f7")


sender = "Private Person <from@smtp.mailtrap.io>"
receiver = "A Test User <to@smtp.mailtrap.io>"

class student(object):

    @staticmethod
    @jwt_required
    def student_dashboard():
        token = get_jwt_identity()
        if token["is_student"] is True:
            student = Student.query.filter_by(unique_id=token["unique_id"]).first()
            if student is None:
                return jsonify(message="Student not found!"), 404
            else:
                result = student_schema.dump(student)
                return jsonify(result), 200

    @staticmethod
    @jwt_required
    def students():
        token = get_jwt_identity()
        if "is_admin" in token:
            if token["is_admin"] is True and token["is_active"] is True:
                students = Student.query.all()
                if len(students) > 0:
                    result = student_schemas.dump(students)
                    return jsonify(
                        status=200,
                        result=result
                    ), 200
                else:
                    return jsonify(
                        status=204,
                        message="No student to display!"
                    ), 204

    @staticmethod
    def student(id:int):
        student = Student.query.filter_by(id=id).first()
        result = student_schema.dump(student)
        if student:
            return jsonify(result),200
        else:
            return jsonify(message="Student Not Found"),404

    @staticmethod
    @jwt_required
    def create():
        token = get_jwt_identity()
        new_student = Student(str(request.get_json()["unique_id"]),str(request.get_json()["f_name"]),
                      str(request.get_json()["m_name"]),str(request.get_json()["l_name"]),str(request.get_json()["gender"]),
                      str(request.get_json()["primary_contact"]),str(request.get_json()["secondary_contact"]),
                      str(request.get_json()["email"]),request.get_json()["password"])

        """
            This will check if a Student already exists 
            with the given Unique Id or Email
        """
        student = Student.query.filter_by(unique_id=request.get_json()["unique_id"]).first() or Student.query.filter_by(email= request.get_json()["email"]).first()
        if "is_admin" in token:
            if token["is_admin"] is True:
                if student is not None:
                    return jsonify(message="Student Already Exists")
                else:
                    db.session.add(new_student)
                    db.session.commit()
                    session['unique_id'] = new_student.unique_id
                    return jsonify(message="Student created successfully"),201
        elif "is_staff" in token:
            if token["is_staff"] is True and token["is_active"] is True:
                if student is not None:
                    return jsonify(message="Student Already Exists")
                else:
                    db.session.add(new_student)
                    db.session.commit()
                    session['unique_id'] = new_student.unique_id
                    return jsonify(message="Student created successfully"),201

    @staticmethod
    def login():
        unique_id = request.get_json()["unique_id"]
        password = request.get_json()["password"]

        if not unique_id:
            return jsonify(message="Please Enter Student's Unique Id or Email"), 400
        if not password:
            return jsonify({"msg": "Missing password "}), 400

        student = Student.query.filter_by(unique_id=unique_id).first()

        if student is not None and student.check_password(password):
            token = create_access_token(identity= {"unique_id": student.unique_id,"is_student":student.is_student})
            refresh_token = create_refresh_token(student.unique_id)
            resp = make_response({
                "status": 200,
                "message": "Login Successful",
                "token": token
            })
            resp.set_cookie('token',token)
            resp.set_cookie('refresh_token',refresh_token)
            return resp

        else:
            return jsonify(message="Invalid username or password"), 401

    @staticmethod
    @jwt_required
    def update(id:int):
        student = Student.query.filter_by(id=id).first()
        token = get_jwt_identity()
        if student is not None:
            unique_id = str(request.get_json()["unique_id"])
            f_name = str(request.get_json()["f_name"])
            m_name = str(request.get_json()["m_name"])
            l_name = str(request.get_json()["l_name"])
            email = str(request.get_json()["email"])
            password = str(request.get_json()["password"])

            student.unique_id = unique_id
            student.F_name = f_name
            student.m_name = m_name
            student.l_name = l_name
            student.email = email
            student.pwdhash = Student.set_password(password)

        if "is_admin" in token:
            if token["is_admin"] is True and token["is_active"]:
                db.session.commit()
                return jsonify(message="Successfully Updated"), 202
            else:
                return jsonify(message="Update Failed"), 401
        elif "is_staff" in token:
            if token["is_staff"] is True and token["is_staff"]:
                db.session.commit()
                return jsonify(message="Successfully Updated"), 202
            else:
                return jsonify(message="Update Failed"), 401
        else:
            return jsonify(status=401,message="Unauthorized Access!"), 401

    @staticmethod
    def logout():
        session.pop('unique_id', None)
        return jsonify("logout successful")

    @staticmethod
    @jwt_required
    def delete(id:int):
        student = Student.query.filter_by(id=id).first()
        get_jwt_identity()
        db.session.delete(student)
        db.session.commit()
        return jsonify(message="Student Deleted Successfully"),209

    @staticmethod
    def password_reset():
        email = str(request.get_json()["email"])
        student = Student.query.filter_by(email=email).first()
        if student:
            # message = "You password is: "
            # sender = "admin@admin.com"
            # smtpObj.sendmail(sender, email, message)
            # msg = Message('Hello', sender='yourId@gmail.com', recipients=[email])
            # msg.body = "This is the email body"
            # mail.send(msg)
            message = "Hi Mailtrap"
            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login("046c0d3e002858", "4424339fab32f7")
                server.sendmail(sender, receiver, message)
                return jsonify(message="Your pasword send to: " + email)
        else:
            print("Error: unable to send email")
