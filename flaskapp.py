import os
from flask import Flask, send_from_directory

from tripleoci import config
app = Flask(__name__)

work_dir = os.path.dirname(__file__)


@app.route('/')
def hello_world():
    return send_from_directory(
        os.path.dirname(config.INDEX_HTML), 'index.html')

if __name__ == '__main__':
    app.run()
