from flask import Blueprint, render_template

visibility_bp = Blueprint('visibility', __name__)

@visibility_bp.route('/visibility')
def visibility():
    return render_template('visibility.html')