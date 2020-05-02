from flask import Flask, Blueprint
from flask_restful import Api
from flask_cors import CORS
from Utils import ErrorHandler

# create application
app = Flask(__name__, template_folder='Views/UI', static_folder='Views/UI/static')
app.config.from_pyfile('config.py')

# instantiate the error handler
errorHandler = ErrorHandler()

# create api blueprint
ApiBP = Blueprint('ApiBP', __name__, url_prefix='/api')
cors = CORS(ApiBP, resources={r"/*": {"origins": "*"}})
api = Api(ApiBP)
app.register_blueprint(ApiBP)

# start controllers
from Controllers import start_controllers
start_controllers(app, api)

# start views
from Views import start_view
start_view(app)

#from Models import Engine, Base
#Base.metadata.drop_all(Engine)
#Base.metadata.create_all(Engine)


if __name__ == "__main__":
    app.run()