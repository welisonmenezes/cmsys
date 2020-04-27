from flask import current_app, Blueprint, render_template, request, url_for, redirect, flash, session, jsonify
from app import app
from Modules.Database import Session

DashboardController = Blueprint('DashboardController', __name__, url_prefix='/admin', template_folder='Views', static_folder='static')

@DashboardController.route('/')
def index():
    return render_template('index.html')