from flask import request, session
from flask import redirect,jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)

from config import db

# Imported Database
from ..models.model import SuperAdmin
from ..models.model import super_admin_schema
from ..models.model import super_admins_schema


class SuperAdminView(object):

    # @SuperAdmin.route('/SuperAdmin/dashboard')
    @staticmethod
    @jwt_required
    def dashboard():
        token = get_jwt_identity()
        if token["super_admin"] is True:
            user = SuperAdmin.query.filter_by(email=token["email"]).first()
            if user:
                result = super_admin_schema.dump(user)
                return jsonify(result), 200
            else:
                return "no user",401

    @staticmethod
    def signup():
        user = SuperAdmin(str(request.get_json()["username"]),str(request.get_json()["name"]),
                str(request.get_json()["email"]),request.get_json()["password"])
        db.session.add(user)
        db.session.commit()
        session['email'] = user.email
        token = create_access_token(identity=user.email)
        return jsonify(session['email']), 201

    @staticmethod
    def login():
        email = request.get_json()["email"]
        password = request.get_json()["password"]
        user = SuperAdmin.query.filter_by(email=email).first()
        if user is not None and user.check_password(password):
            token = create_access_token(identity= {
                "email": user.email,
                "is_active": user.is_active,
                "is_admin": user.is_admin,
                "is_staff": user.is_staff,
                "is_super_admin": user.is_super_admin
               })
            return jsonify(token), 200
        else:
            return jsonify({"msg": "Invalid username or password"}), 401

    # update SuperAdmin
    @staticmethod
    @jwt_required
    def update(id:int):
        user = SuperAdmin.query.filter_by(id=id).first()
        get_jwt_identity()
        if user is None:
            username = str(request.get_json()["username"])
            name = str(request.get_json()["name"])
            email = str(request.get_json()["email"])
            password = str(request.get_json()["password"])

            user.username = username
            user.name = name
            user.email = email
            user.pwdhash = SuperAdmin.set_password(password)

            db.session.commit()
            return jsonify(message="Successfully Updated"), 202
        else:
            return jsonify(message="Super Admin not found."), 401

    # @SuperAdmin.route('/SuperAdmin/logout')
    @staticmethod
    def logout():
        session.pop('email', None)
        return jsonify("logout successful")

    @staticmethod
    @jwt_required
    def delete(id:int):
        user = SuperAdmin.query.filter_by(id=id).first()
        get_jwt_identity()
        db.session.delete(user)
        db.session.commit()
        return jsonify(message="Delete Successful"),209
