import hashlib
import logging
import os
import smtplib
import ssl

import flask
from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app, support_credentials=True)

logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def root():
    """
    The default root route, it shows nothing so far, just checking that the connection works.
    :return: A text string notifying it works.
    """
    return 'It works!'


@app.route('/register', methods=['GET', 'POST'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def register():
    """
    Registers the email of a user that will select to download the binary packages of the latest release candidate.
    :return: A success notification if it works or an error message if it fails.
    """
    if 'email' in request.args:
        email_arg = request.args['email']
        user = find_user(email_arg)
        if user == "":
            return register_email(email_arg)
        else:
            return verify_redirect(user)
    else:
        return page_not_found()


def find_user(email):
    if os.path.exists('data'):
        users_list = os.listdir('data')
        if users_list.__len__() > 0:
            for user in users_list:
                with open(os.path.join('data/', user), 'r') as f:
                    email_str = f.readline()
                    if email == email_str.strip():
                        return user
                    else:
                        return ""
        else:
            return register_email(email)
    else:
        os.makedirs('data')
        return ""


def register_email(email):
    encoded_email = create_hash_code(email)
    # Send confirmation email
    smtp_server = os.environ.get("SMTP_SERVER")
    port = os.environ.get("SMTP_PORT")
    sender_email = os.environ.get("CONTACT_EMAIL")
    password = os.environ.get("CONTACT_PASS")
    message = MIMEMultipart("alternative")
    message["Subject"] = "Thank you for registering on LizardFS"
    message["From"] = sender_email
    message["To"] = email
    verification_url = os.environ.get("API_URL") + 'verify?code=' + encoded_email.hexdigest()
    html = """\
        <html>
            <body>
                <p>
                    Click on the link below to access the download page for packages.
                </p>
                
                <p>
                    <a href="%s">Verify email</a>
                </p>
            </body>
        </html>
        """ % verification_url
    message.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, int(port), context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, email, message.as_string())

    # Store the information in the DB
    new_user = open('data/' + encoded_email.hexdigest(), "a")
    new_user.write(email + '\n')
    return "User registered with hash code: " + encoded_email.hexdigest()


def create_hash_code(email):
    email_code = email + "hydra"
    encoded_email = hashlib.md5(email_code.encode())
    return encoded_email


def page_not_found():
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/verify', methods=['GET'])
@cross_origin(origin='*', headers=['Content- Type', 'Authorization'])
def verify():
    """
    Verifies that the code sent from the verification link sent by email is valid, and activates the user.
    :return: A text string notifying it works.
    """
    if 'code' in request.args:
        code = request.args['code']
        users_list = os.listdir('data')
        for user in users_list:
            if user == code:
                with open(os.path.join('data/', user), 'a') as f:
                    f.write("valid" + '\n')
        return verify_redirect(code)
    else:
        page_not_found()


def verify_redirect(code):
    if check_valid(code):
        packages = os.environ.get("PACKAGES_URL")
        return flask.redirect(packages)
    else:
        registration = os.environ.get("LFS_REGISTRATION")
        return flask.redirect(registration)


def check_valid(code):
    users_list = os.listdir('data')
    for user in users_list:
        if user == code:
            with open(os.path.join('data/', user), 'r') as f:
                return 'valid' in f.read()


if __name__ == '__main__':
    app.run()
