from flask import Flask

app = Flask(__name__)


@app.route('/')
def root():  # put application's code here
    return 'It works!'


@app.route('/register')
def register():  # put application's code here
    # take the email received by parameter
    return 'Email to register'


if __name__ == '__main__':
    app.run()
