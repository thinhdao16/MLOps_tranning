from flask import Blueprint
from controller.uv_controller import uv as uv_controller

uv_bp = Blueprint('uv', __name__)

@uv_bp.route('/uv', methods=['GET', 'POST'])
def uv():
    return uv_controller()