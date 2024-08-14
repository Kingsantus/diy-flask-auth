# Flask Authentication System builing from scratch

This is an authentication system for python flask api. the sole purpose is to give an insight about the behind the hook what happens in the backround when you utilize Flask-User module.

## Table of Content

- [Project Name](#flask-authentication-system-builing-from-scratch)
- [Cloning the project](#cloning-the-project)
- [Installing Requirements](#installing-the-requirement)

## cloning the project

To get a copy of this project up and running on your local machine, you the following command:

```bash
git clone https://github.com/kingsantus/diy-flask-auth.git
```

## Installing the Requirement
```python
pip install -r requirements.txt
```

## Project Overview

The project is broken down into 5 major different files.
- auth.py
intermediate between db.py and routes in app.py
- main.py
a test file for the routes specified in app.py
- app.py
it handles the routes of the API for creating user, logout, gettting session id and resetting password
- db.py
contains fuction that interacts with the database.
- user.py
contains the sql code to create a simple user"# diy-flask-auth" 
