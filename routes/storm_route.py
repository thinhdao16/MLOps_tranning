from flask import Blueprint, render_template

storm_bp = Blueprint('storm', __name__)

@storm_bp.route('/storm')
def storm():
    return render_template('storm.html')