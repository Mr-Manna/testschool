from flask import request
from flask import jsonify
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)
import smtplib

from config import db

from ..models.academic import AcademicInfo,academic_schemas


class AcademicProfile(object):

    @staticmethod
    @jwt_required
    def profiles(id:int):
        token = get_jwt_identity()
        if "is_admin" in token:
            if token["is_admin"] is True and token["is_active"] is True:
                academic = AcademicInfo.query.filter_by(student_id=id)
                results = academic_schemas.dump(academic)
                if results:
                    return jsonify(
                        results=results,
                        status=200,
                        response="ok"
                    ), 200
                else:
                    return jsonify(
                        message="No result found",
                        status=204,
                        response="ok"
                    ), 204
            else:
                return jsonify(message="Please login to access this page")

    @staticmethod
    @jwt_required
    def create_profile(id: int):
        token = get_jwt_identity()
        if "is_admin" in token:
            if token["is_admin"] is True:
                new_profile = []
                profiles = request.get_json()

                for i in profiles:
                    obj = AcademicInfo(i["session"], i["roll_no"], i["standard"], i["section"], i["fee_type"],
                                       i["student_id"])
                    new_profile.append(obj)

                try:
                    db.session.add_all(new_profile)
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to add profile"), 404
                finally:
                    return jsonify(message="Profile created successfully"), 201

        else:
            return jsonify(
                status=401,
                message="Unauthorized Access",
                response="ok"
            ), 401

    @staticmethod
    @jwt_required
    def update_profile(id:int):
        token = get_jwt_identity()
        academic = AcademicInfo.query.filter_by(student_id=id).first()

        if "is_admin" in token:
            if token["is_admin"] is True:
                try:
                    academic.sesson = str(request.get_json()["session"])
                    academic.roll_no = str(request.get_json()["roll_no"])
                    academic.standard = int(request.get_json()["standard"])
                    academic.section = str(request.get_json()["section"])
                    academic.fee_type = str(request.get_json()["fee_type"])
                    academic.student_id = int(request.get_json()["student_id"])
                    db.session.commit()
                except ValueError:
                    return jsonify(message="Unable to update profile"),404
                else:
                    return jsonify(message="Profile updated successfully"),201
        else:
            return jsonify(
                status=401,
                message="Unauthorized Access",
                response="ok"
            ), 401
