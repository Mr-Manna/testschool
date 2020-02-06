from flask import request, session
from flask import jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
import os
from werkzeug.utils import secure_filename

from config import db,app
from config import UPLOADS

from apps.super_admin.models.model import SuperAdmin
from ..models.student import Student
from ..models.personal import StudentAddress,StudentAvatar
from ..models.personal import student_addresses_schema,student_avatar_schema


class PersonalInfo(object):

    @staticmethod
    @jwt_required
    def addresses(id:int):
        token = get_jwt_identity()
        if "is_student" in token:
            if token["is_student"] is True:
                addresses = StudentAddress.query.filter_by(student_id=id)
                result = student_addresses_schema.dump(addresses)
                return jsonify(status=200, result=result), 200
        elif "is_admin" in token:
            if token["is_admin"] is True:
                addresses = StudentAddress.query.filter_by(student_id=id)
                result = student_addresses_schema.dump(addresses)
                return jsonify(status=200, result=result), 200
        else:
            return jsonify(message="You are not authorized"), 401

    @staticmethod
    @jwt_required
    def create_address(id:int):
        token = get_jwt_identity()
        new_address = []
        addresses = request.get_json()
        for i in addresses:
            obj = StudentAddress(str(i["address_type"]), str(i["location"]),str(i["pincode"]),str(i["city"]),
                                 str(i["state"]), int(i["student_id"]))
            new_address.append(obj)

        if "is_student" in token:
            if token["is_student"] is True:
                try:
                    db.session.add_all(new_address)
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to add address")
                else:
                    return jsonify(message="Student's address created successfully"),201
        elif "is_admin" in token:
            if token["is_admin"] is True:
                try:
                    db.session.add_all(new_address)
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to add address")
                else:
                    return jsonify(message="Student's address created successfully"),201
        else:
            return jsonify(status=401,message="Unauthorized Access")

    @staticmethod
    @jwt_required
    def update_address(id:int):
        address = StudentAddress.query.filter_by(id=id).first()
        token = get_jwt_identity()
        if address is not None:
            update = request.get_json()
            address.address_type = update["address_type"]
            address.location = update["location"]
            address.pincode = update["pincode"]
            address.city = update["city"]
            address.state = update["state"]
            address.student_id = update["student_id"]

        while "is_student" in token:
            if token["is_student"] is True:
                db.session.commit()
                return jsonify(message="Successfully Updated"), 202
            else:
                return jsonify(message="Address not found"), 404

        while "is_admin" in token:
            if token["is_admin"] is True:
                if token["is_admin"] is True:
                    db.session.commit()
                    return jsonify(message="Successfully Updated"), 202
                else:
                    return jsonify(message="Address not found"), 404

    @staticmethod
    @jwt_required
    def delete_address(id:int):
        token = get_jwt_identity()
        if "is_student" in token:
            if token["is_student"] is True:
                try:
                    address = StudentAddress.query.filter_by(id=id).first()
                    db.session.delete(address)
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to delete addresses")
                else:
                    return jsonify(message="Address deleted successfully"), 209
        elif "is_admin" in token:
            if token["is_admin"] is True:
                try:
                    address = StudentAddress.query.filter_by(id=id).first()
                    db.session.delete(address)
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to delete addresses")
                else:
                    return jsonify(message="Address deleted successfully"), 209
        else:
            return jsonify(staus=401, message="Unauthorized Access"), 401


class StudentAvatarView(object):

    @staticmethod
    def upload_avatar():
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
