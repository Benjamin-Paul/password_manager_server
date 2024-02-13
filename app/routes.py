from flask import request, jsonify
import jwt
import datetime as dt
import pickle
import json
from collections import namedtuple

from noknow import ZK, ZKSignature, ZKData

from app import app, db
from app.models import User, Safe
from app.auth.jwt import token_required
from app.auth.zk_auth import create_server_signature, create_zk_instance, send_random_token, process_proof

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
            return jsonify(success=False, content="This user already exists.")
        db.session.add(new_user)
        db.session.commit()
        return jsonify(success=True, content=f"New user added : {user_name}.")

@app.route("/login", methods=["GET", "POST"])
def login():       
    if "user" in request.form:
        user_name = request.form["user"]
        user = User.query.filter_by(user=user_name).first()
        if user is None:
            return jsonify(success=False, content="Wrong credentials.")
        if "token" in request.form:
            try:
                data = jwt.decode(request.form["token"], app.jwt_signing_key, algorithms="HS256")
                if data["user"] == user_name:
                    return jsonify(success=False, content="You're already logged in.")
            except:
                pass
        # zero-knowledge proof verification
        client_signature = user.signature.strip("\"")
        client_signature = ZKSignature.load(client_signature)
        zk_server, server_signature = create_server_signature()
        zk_client = create_zk_instance(client_signature)
        signa_str = json.dumps(server_signature.dump())
        user.serversignature = signa_str
        db.session.commit()
        print(client_signature.dump())
        print(type(client_signature.dump()))
        return jsonify(success=True, content=send_random_token(zk_server, zk_client), sig=client_signature.dump())
    return jsonify(success=False, content="Provide a POST request with a username value.")

@app.route("/proof", methods=["POST"])
def proof():
    if "user" in request.form:
        user_name = request.form["user"]
        user = User.query.filter_by(user=user_name).first()
        if user is None:
            return jsonify(success=False, content="Wrong credentials.")
        else:
            proof = request.form["proof"]
            server_signature = ZKSignature.load(user.serversignature.strip("\""))
            zk_server = ZK(server_signature.params)
            client_signature = user.signature.strip("\"")
            client_signature = ZKSignature.load(client_signature)
            zk_client = ZK(client_signature.params)
            if process_proof(proof, zk_server, server_signature, zk_client, client_signature):
                jwt_token = jwt.encode({'user': user_name, 'exp': dt.datetime.utcnow() + dt.timedelta(hours=1)}, app.jwt_signing_key)
                return jsonify(success=True, content=jwt_token)
            else:
                return jsonify(success=False, content="Wrong credentials.")

@app.route("/get", methods=["POST"])
@token_required
def get_password(current_user):
    user_rows = Safe.query.filter_by(owner=current_user.user).all()
    list_of_sites = []
    for row in user_rows:
        list_of_sites.append(row.site)
    if "site" not in request.form:
        return jsonify(success=True, content=list_of_sites)
    requested_site = request.form["site"]
    if requested_site in list_of_sites:
        row_fetched = Safe.query.filter_by(owner=current_user.user, site=requested_site).first()
        return jsonify(success=True, content=[row_fetched.password, row_fetched.username])
    return jsonify(success=True, content=list_of_sites)

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