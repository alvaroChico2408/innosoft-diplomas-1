from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.modules.diplomas import diplomas_bp
from app.modules.diplomas.forms import UploadExcelForm
from app.modules.diplomas.services import DiplomasService

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
        return redirect(url_for('diplomas.index'))
    
    return render_template('diplomas/index.html', form=form)


