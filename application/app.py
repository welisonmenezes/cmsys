from flask import Flask, render_template, redirect, url_for

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_pyfile('config.py')

from Controllers import *

app.register_blueprint(DashboardController)



from Models import Engine, Base
#Base.metadata.drop_all(Engine)
#Base.metadata.create_all(Engine)



if __name__ == "__main__":
    app.run()