from flask import Flask

app = Flask(__name__)

app.secret_key= b'e128l23d95e34r5435#OA12vs32xSF*'

from controllers import *

if __name__ == "__main__":
    app.run(debug=True)