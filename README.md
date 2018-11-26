# flask-template

[![Build Status](https://travis-ci.com/ltaniguti/flask-template.svg?branch=master)](https://travis-ci.com/ltaniguti/flask-template)  [![codecov](https://codecov.io/gh/ltaniguti/flask-template/branch/master/graph/badge.svg)](https://codecov.io/gh/ltaniguti/flask-template)  [![Maintainability](https://api.codeclimate.com/v1/badges/58781f4fb4ba514471f8/maintainability)](https://codeclimate.com/github/ltaniguti/flask-template/maintainability)


Application template using flask and JWT authentication.

## Quick start

Run de application

```bash
pip install -r requirements
FLASK_APP=escola.py
flask db upgrade
flask run
```

Interact with it

```bash
# Register
curl -X POST \
     -d '{"email":"my@email.com", "password":"1234"}' \
     -H "Content-Type: application/json" http://localhost:5000/auth/register
     
# Output:
# {"auth_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NDMwNzc5MjcsImlhdCI6MTU0MzA3NzkyMiwic3ViIjoxfQ.dPmFuSx9diBHcWjWMWPc5hhNHOmxx3axSx8T9hjFNkk","message":"Successfully registered.","status":"success"}

# Login
curl -X POST \
     -d '{"email":"my@email.com", "password":"1234"}' \
     -H "Content-Type: application/json" http://localhost:5000/auth/login

# Protected route
curl -X GET \
     -d '{"email":"my@email.com", "password":"1234"}' \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer <auth_token_previously_returned>" http://localhost:5000/auth/status

```
