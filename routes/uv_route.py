from flask import Blueprint, render_template

uv_bp = Blueprint('uv', __name__)

@uv_bp.route('/uv')
def uv():
    return render_template('uv.html')