from flask import Flask

app = Flask(__name__)

from scotcovidapp import routes
