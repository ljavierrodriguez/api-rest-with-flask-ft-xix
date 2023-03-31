from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db
from config import DevelopmentConfig
from routes import main, users

app = Flask(__name__)
app.config.from_object(DevelopmentConfig()) # Configuracion desde archivo config.py
db.init_app(app)
Migrate(app, db) # db init, db migrate, db upgrade, db downgrade
CORS(app)

app.register_blueprint(main.bpMain)
app.register_blueprint(users.bpUser, url_prefix='/api')

if __name__ == '__main__':
    app.run()