from flask import Flask

app = Flask(__name__)

from advice_web.routes import views