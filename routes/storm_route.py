from flask import Blueprint
from controller.storm_controller import storm as storm_controller

storm_bp = Blueprint('storm', __name__)

@storm_bp.route('/storm', methods=['GET', 'POST'])
def storm():
    return storm_controller()