from flask import Flask, render_template
from os import getenv
from datetime import datetime

app = Flask(__name__, template_folder='.')
CSRF_ENDPOINT = getenv('CSRF_ENDPOINT', "http://127.0.0.1/csrf-attack")


@app.route('/')
def index():
    return render_template(
        './index.html',
        csrf_endpoint=CSRF_ENDPOINT,
        timestamp=datetime.now(),
    )


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=8000,
        debug=True,
    )
