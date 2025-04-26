from flask import Blueprint
from controller.rainfall_controller import rainfall as rainfall_controller

rainfall_bp = Blueprint('rainfall', __name__)

@rainfall_bp.route('/rainfall', methods=['GET', 'POST'])
def rainfall():
    return rainfall_controller()