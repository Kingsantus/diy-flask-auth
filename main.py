#!/usr/bin/env python3
"""
Main file
"""
import requests
import json


# establishing the url to be used by request
BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    """Testing creating user using request module"""
    resp = requests.post(f'{BASE_URL}/users/', data={'email': email, 'password': password})
    assert resp.status_code == 201
    assert resp.json() == {'email': email, 'message': 'user created'}

def log_in_wrong_password(email: str, password: str) -> None:
    """Testing Logining in a wrong credential  for user"""
    resp = requests.post(f'{BASE_URL}/sessions/', data={'email': email, 'password': password})
    assert resp.status_code == 401

def log_in(email: str, password: str) -> str:
    """Testing loging a user in while testing the statuscode and return string"""
    resp = requests.post(f'{BASE_URL}/sessions/', data={'email': email, 'password': password})
    assert resp.status_code == 200
    return resp.cookies.get('session_id')

def profile_unlogged() -> None:
    """Testing check for session_id in the cookie"""
    resp = requests.get(f'{BASE_URL}/profile/')
    # check if session_id not found will return 403
    assert resp.status_code == 403

def profile_logged(session_id: str) -> None:
    """Testing get the user session id generated after login"""
    resp = requests.get(f'{BASE_URL}/profile/', cookies={"session_id":session_id})
    assert resp.status_code == 200
    assert 'email' in resp.json()
    
def log_out(session_id: str) -> None:
    """Testing logging out a user using the session_id generated after the login in"""
    resp = requests.delete(f'{BASE_URL}/sessions/', cookies={"session_id":session_id})
    assert resp.status_code == 200

def reset_password_token(email: str) -> str:
    """Testing existing user email will generate a reset token for the user"""
    resp = requests.post(f'{BASE_URL}/reset_password/', data={"email":email})
    assert resp.status_code == 200
    return resp.json().get("reset_token")

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Testing updating user password with the token generated from reset password, email and new_password"""
    resp = requests.put(f'{BASE_URL}/reset_password/', data={"email":email, "reset_token": reset_token, "new_password": new_password})
    assert resp.status_code == 200
    assert resp.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)