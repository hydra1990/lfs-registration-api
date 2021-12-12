from flask import Flask
from flask import request
import os
import base64
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def root():
    """
    The default root route, it shows nothing so far, just checking that the connection works.
    :return: A text string notifying it works.
    """
    return 'It works!'


@app.route('/register', methods=['GET'])
def register():
    """
    Registers the email of a user that will select to download the binary packages of the latest release candidate.
    :return: A text string notifying it works.
    """
    if 'email' in request.args:
        email_arg = request.args['email']
        users_list = os.listdir('data')
        if users_list.__sizeof__() > 0:
            if email_exists(email_arg):
                # success. redirect to the binary packages site
                return "Success!! Email: " + email_arg
            else:
                return register_email(email_arg)
        else:
            return register_email(email_arg)
    else:
        return page_not_found()


def register_email(email):
    return "That email is not in the DB: " + email


def email_exists(email):
    exists = 0
    users_list = os.listdir('data')
    app.logger.info(users_list)
    for user in users_list:
        app.logger.info(user)
        with open(os.path.join('data/', user), 'r') as f:
            email_str = f.read()
            app.logger.info(email_str)
            if email == email_str:
                exists = 1
    return bool(exists)


def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


def create_hash_code(email: str):
    return base64.standard_b64encode(bytearray(email + 'hydra'))


if __name__ == '__main__':
    app.run()
