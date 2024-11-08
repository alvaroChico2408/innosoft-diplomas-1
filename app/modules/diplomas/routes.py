from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.modules.diplomas.models import Diploma
from app.modules.diplomas import diplomas_bp
from app.modules.diplomas.forms import UploadExcelForm
from app.modules.diplomas.services import DiplomasService
import os
from flask import send_file
from flask import current_app
from app import db

diplomas_service = DiplomasService()


@diplomas_bp.route('/diplomas', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadExcelForm()
    
    if form.validate_on_submit():
        file = form.hours_excel.data
        if file:
            try:
                diplomas_service.validate_and_save_excel(file)
                flash("Diplomas generados con éxito", "success")
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}", "error")
        return render_template('diplomas/index.html', form=form)
    
    return render_template('diplomas/index.html', form=form)


@diplomas_bp.route('/diplomas-visualization', methods=['GET'])
@login_required
def diplomas_visualization():
    diplomas = Diploma.query.all()
    return render_template('diplomas/diplomas-visualization.html', diplomas=diplomas)


@diplomas_bp.route('/view_diploma/<int:diploma_id>', methods=['GET'])
@login_required
def view_diploma(diploma_id):
    diploma = Diploma.query.get(diploma_id)
    if diploma and diploma.file_path:
        file_path = os.path.join(current_app.root_path, "..", "diplomas", os.path.basename(diploma.file_path))
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            flash("The diploma file could not be found.", "error")
    else:
        flash("The diploma could not be found.", "error")
    return redirect(url_for("diplomas.diplomas_visualization"))

@diplomas_bp.route('/delete_diploma/<int:diploma_id>', methods=['POST'])
@login_required
def delete_diploma(diploma_id):
    if request.form.get('_method') == 'DELETE':
        try:
            diploma = Diploma.query.get(diploma_id)
            if diploma:
                file_path = os.path.join(current_app.root_path, "..", "diplomas", os.path.basename(diploma.file_path))
                if os.path.exists(file_path):
                    os.remove(file_path)
                db.session.delete(diploma)
                db.session.commit()
                flash("Diploma deleted successfully.", "success")
            else:
                flash("Diploma not found.", "error")
        except Exception as e:
            flash(f"Error deleting diploma: {e}", "error")
    return redirect(url_for("diplomas.diplomas_visualization"))


