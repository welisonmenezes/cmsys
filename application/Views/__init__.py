from flask import Blueprint, render_template

def start_view(app):

    # route to admin ui interface (that's a react SPA aplication)
    AdminBP = Blueprint('AdminBP', __name__, url_prefix='/')
    @AdminBP.route('/', defaults={'path': ''})
    @AdminBP.route('/<path:path>')
    def index(path):
        return render_template('index.html'), 200
    app.register_blueprint(AdminBP)