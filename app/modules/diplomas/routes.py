from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.modules.diplomas import diplomas_bp

@diplomas_bp.route('/diplomas', methods=['GET'])
def index():
    return render_template('diplomas/index.html')

@diplomas_bp.route('/diplomas/generate', methods=['POST'])
@login_required
def generate():
    print("¡Botón de generar diploma pulsado!")
    print("Todo perfecto")
    return redirect(url_for('diplomas.index'))
