from flask import Blueprint

views = Blueprint('views', __name__)


@views.route('/')
def index():
    return "homepage"

@views.route('/track')
def track():
    return "track"