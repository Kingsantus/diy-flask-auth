#!/usr/bin/env python3
"""Flask running the server side
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)

AUTH = Auth()

@app.route('/', methods=['GET'], strict_slashes=False,)
def index() -> str:
    """Method for index route"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route('/users/', methods=['POST'], strict_slashes=False,)
def users() -> tuple:
    """User registration route"""
    
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    try:
        
        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    

@app.route('/sessions/', methods=['POST'], strict_slashes=False,)
def login() -> tuple:
    """Handles the login or create session for user"""
    # get email and password from the input
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    
    # utilize valid_login to check if the password and email are exactly what in the database or abort
    if not AUTH.valid_login(email, password):
        abort(401)

    # create a session id for the login user
    session_id = AUTH.create_session(email)

    # utilizing the session id and set it to a cookie
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)

    return resp


@app.route('/sessions/', methods=['DELETE'], strict_slashes=False,)
def logout():
    """Logout user destroying the session id"""
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)

    response = redirect('/') # redirect user to /
    response.delete_cookie('session_id') # removing the cookies also
    return response

@app.route('/profile/', methods=['GET'], strict_slashes=False,)
def profile() -> jsonify:
    """Get the user login with the cookiee"""
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200

@app.route('/reset_password/', methods=['POST'], strict_slashes=False,)
def get_reset_password_token() -> str:
    """Generates a token that will help for reset email"""
    email = request.form.get('email')

    if email is None:
        abort(403)
    
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": token,}), 200


@app.route('/reset_password/', methods=['PUT'])
def update_password():
    """Update the new password using email, reset_token and the new password."""

    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')
    
    if not email or not reset_token or not new_password:
        abort(400)
    
    try:
        # check if the token is valid and update it with
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        # If the token is invalid, respond with 403 Forbidden
        abort(403)
    
    # Return a JSON response indicating success
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")