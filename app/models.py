from app import db

class Safe(db.Model):
    __tablename__ = 'safe'

    #TODO modify database to host nonce and tag for decryption
    site = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    owner = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)

class User(db.Model):
    __tablename__ = 'users'

    user = db.Column(db.String, primary_key=True)
    signature = db.Column(db.String)
    serversignature = db.Column(db.String)