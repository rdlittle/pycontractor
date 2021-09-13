import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from contractor import app

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8181)
