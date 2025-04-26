from flask import Blueprint, render_template

rainfall_bp = Blueprint('rainfall', __name__)

@rainfall_bp.route('/rainfall')
def rainfall():
    return render_template('rainfall.html')