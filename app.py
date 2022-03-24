# Author: Chi Zhang z5211214
# Date: 22/02/2022

from flask import Flask
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run("0.0.0.0", debug=True)
