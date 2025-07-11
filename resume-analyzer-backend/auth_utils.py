from functools import wraps
from flask import request, jsonify, current_app
import jwt
from flask_sqlalchemy import SQLAlchemy
from models import db,User
db = SQLAlchemy()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            token = token.split(" ")[1]  # Bearer <token>
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return jsonify({"message": "User not found"}), 401

        except Exception as e:
            return jsonify({"message": "Invalid or expired token", "error": str(e)}), 401

        return f(current_user, *args, **kwargs)
    return decorated