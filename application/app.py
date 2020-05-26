from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import datetime

# Create the application
app = Flask(__name__, template_folder='Views/UI', static_folder='Views/UI/static')
app.config.from_pyfile('config.py')
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=30)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(minutes=1)
jwt = JWTManager(app)

# Start the logging
if app.config['ENABLE_LOG_FILE']:
    from Utils import Logger
    Logger(app)

# Create the API and the Blueprint
ApiBP = Blueprint('ApiBP', __name__, url_prefix='/api')
cors = CORS(ApiBP, resources={r"/api/*": {"origins": "*"}})
api = Api(ApiBP)
app.register_blueprint(ApiBP)

# Start the controllers
from Controllers import start_controllers
start_controllers(app, api)

# Start the view
from Views import start_view
start_view(app)

if __name__ == "__main__":
    app.run()