from flask import Flask
from flask import request, jsonify
import os
import subprocess

app = Flask(__name__)


@app.route('/')
def root():
    """
    The default root route, it shows nothing so far, just checking that the connection works.
    :return: A text string notifying it works.
    """
    return 'It works!'


@app.route('/register')
def register():  # put application's code here
    # take the email received by parameter
    return 'Email to register'


if __name__ == '__main__':
    app.run()
