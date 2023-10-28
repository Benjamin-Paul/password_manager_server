from flask import request, jsonify
from functools import wraps
import jwt
import datetime as dt


from app import app, db
from app.models import User, Safe


def token_required(fn):
    @wraps(fn)
    def decorated(*args, **kwargs):
        if "token" in request.form:
            token = request.form["token"]
            try: 
                data = jwt.decode(token, app.jwt_signing_key, algorithms="HS256")
                current_user = User.query.filter_by(user=data["user"]).first()
            except jwt.ExpiredSignatureError:
                return "Your sessions has expired."
            except jwt.DecodeError:
                return "Access denied."
            return fn(current_user, *args, **kwargs)
        else:
            return "Provide username and token to authenticate yourself."
    return decorated

@app.route("/register", methods=["POST"])
def register():
    if "user" and "signature" in request.form:
        user_name = request.form["user"]
        signature = request.form["signature"]
        new_user = User()
        new_user.user = user_name
        new_user.signature = signature
        user = User.query.filter_by(user=user_name).first()
        # TODO add email for recovery and identity check
        if user is not None:
            return "This user already exists."
        db.session.add(new_user)
        db.session.commit()
        return f"New user added : {user_name}. Don't forget your passphrase."

@app.route("/login", methods=["GET", "POST"])
def login():       
    if "secret" and "user" in request.form:
        secret = request.form["secret"]
        user_name = request.form["user"]
        user = User.query.filter_by(user=user_name).first()
        if user is None:
            return "Wrong credentials (user doesn't exist)."
        # TODO implement secret zero-knowledge verification 
        if secret != "good secret":
            return "Wrong credentials (wrong password)."
        if "token" in request.form:
            try:
                data = jwt.decode(request.form["token"], app.jwt_signing_key, algorithms="HS256")
                if data["user"] == user_name:
                    return "You're already logged in."
            except:
                pass
        db.session.commit()
        token = jwt.encode({'user': user_name, 'exp': dt.datetime.utcnow() + dt.timedelta(hours=1)}, app.jwt_signing_key)
        return jsonify({'token': token})
    return "Provide a POST request with secret and username values."

@app.route("/get", methods=["POST"])
@token_required
def get_password(current_user):
    if current_user.user != request.form["user"]:
        return "Access denied."
    user_rows = Safe.query.filter_by(owner=current_user.user).all()
    list_of_sites = []
    for row in user_rows:
        list_of_sites.append(row.site)
    if "site" not in request.form:
        return jsonify({"sites": list_of_sites})
    requested_site = request.form["site"]
    if requested_site in list_of_sites:
        return Safe.query.filter_by(owner=current_user.user, site=requested_site).first().password
    return jsonify("The site you requested doesn't exist.", {"sites": list_of_sites})

@app.route("/add", methods=["POST"])
@token_required
def add_password(current_user):
    if ("site" not in request.form) or ("password" not in request.form):
        return "Incomplete data. Provide at least a site and a password."
    if Safe.query.filter_by(site=request.form["site"], owner=current_user.user).first() is not None:
        return "You already have a password for this site. Use /change to change it."
    new_entry = Safe()
    new_entry.owner = current_user.user
    new_entry.site = request.form["site"]
    new_entry.password = request.form["password"]
    if "username" in request.form:
        new_entry.username = request.form["username"]
    db.session.add(new_entry)
    db.session.commit()
    return "Entry added."

@app.route("/change", methods=["POST"])
@token_required
def change_password(current_user):
    if "site" not in request.form:
        return "Indicate for which site you wish to change credentials."
    if "password" not in request.form:
        return "Indicate new password."
    entry_to_change = Safe.query.filter_by(site=request.form["site"], owner=current_user.user).first()
    entry_to_change.password = request.form["password"]
    db.session.commit()
    return f'Password changed for {request.form["site"]}.' 

@app.route("/delete", methods=["POST"])
@token_required
def delete_entry(current_user):
    if "site" not in request.form:
        return "Indicate for which site you wish to delete credentials."
    entry_to_delete = Safe.query.filter_by(site=request.form["site"], owner=current_user.user).first()
    if entry_to_delete is None:
        return "The profile you are trying to delete doesn't exist."
    db.session.delete(entry_to_delete)
    db.session.commit()
    return f'Profile deleted for {request.form["site"]}.' 