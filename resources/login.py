from flask import Blueprint, request
from model import db, Login
import bcrypt


blp = Blueprint('login', __name__)

@blp.route("/login", methods=['POST'])
def handling_login():
    auth = request.get_json()
    username, password = auth['username'], auth['password']
    login = Login.query.filter_by(username=username).first()
    if login == None:
        return {"message": "Failed. Username is not registered."}
    if bcrypt.checkpw(password.encode('utf-8'), login.password):
        login.is_active = True # login_user(login)
        db.session.commit()
        return {"message": "Success. Username and password are registered."}
    return {"message": "Failed. Password does not match the username."}