import os
from flask import Flask

from tripleoci import config
app = Flask(__name__)

work_dir = os.path.dirname(__file__)

@app.route('/')
def hello_world():
    with open(config.INDEX_HTML) as f:
        return f.read()

if __name__ == '__main__':
    app.run()
