from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '295b73d3ee6a8e1bdde396fa29169164'

from api.routes import views