from flask import request, jsonify
from functools import wraps
import jwt

from app import app
from app.models import User
from app.auth.zk_auth import create_server_signature, create_zk_instance, send_random_token, process_proof

# Decorator function that will be used to set up restricted routes
def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if "token" in request.form:
            token = request.form["token"]
            try: 
                data = jwt.decode(token, app.jwt_signing_key, algorithms="HS256")
                current_user = User.query.filter_by(user=data["user"]).first()
            except jwt.ExpiredSignatureError:
                return jsonify(success=False, content="Your session has expired.")
            except jwt.DecodeError:
                return jsonify(success=False, content="Access denied.")
            return fn(current_user, *args, **kwargs)
        else:
            return jsonify(success=False, content="Provide username and token to authenticate yourself.")
    return decorated