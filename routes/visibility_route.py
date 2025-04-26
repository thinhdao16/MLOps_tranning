from flask import Blueprint
from controller.visibility_controller import visibility as visibility_controller

visibility_bp = Blueprint('visibility', __name__)

@visibility_bp.route('/visibility', methods=['GET', 'POST'])
def visibility():
    return visibility_controller()