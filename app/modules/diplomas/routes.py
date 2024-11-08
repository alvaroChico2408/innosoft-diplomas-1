from flask import render_template
from app.modules.diplomas import diplomas_bp


@diplomas_bp.route('/diplomas', methods=['GET'])
def index():
    return render_template('diplomas/index.html')
