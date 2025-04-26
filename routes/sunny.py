from flask import Blueprint, render_template

sunny_bp = Blueprint('sunny', __name__)

@sunny_bp.route('/sunny')
def sunny():
    return render_template('sunny.html')