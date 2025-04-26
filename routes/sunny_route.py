from flask import Blueprint
from controller.sunny_controller import sunny as sunny_controller

sunny_bp = Blueprint('sunny', __name__)

@sunny_bp.route('/sunny', methods=['GET', 'POST'])
def sunny():
    return sunny_controller()