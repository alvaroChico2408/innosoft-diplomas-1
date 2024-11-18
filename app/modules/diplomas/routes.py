from flask import render_template, redirect, url_for, flash, request, jsonify, send_file, current_app
from flask_login import login_required
from app.modules.diplomas.models import Diploma, DiplomaTemplate
from app.modules.diplomas import diplomas_bp
from app.modules.diplomas.forms import UploadExcelForm, UploadTemplateForm
from app.modules.diplomas.services import DiplomasService
import os
from app import db, mail_service



diplomas_service = DiplomasService()


@diplomas_bp.route('/diplomas', methods=['GET', 'POST'])
@login_required
def index():
    form = UploadExcelForm()
    
    if form.validate_on_submit():
        file = form.hours_excel.data
        selected_template_id = form.template.data
        if file and selected_template_id:
            try:
                template = DiplomaTemplate.query.get(selected_template_id)
                diplomas_service.validate_and_save_excel(file, template)
                flash("Diplomas generados con éxito", "success")
            except Exception as e:
                flash(f"Error al procesar el archivo: {str(e)}", "error")
        return redirect(url_for('diplomas.index'))
    return render_template('diplomas/index.html', form=form)


@diplomas_bp.route('/diplomas-visualization', methods=['GET'])
@login_required
def diplomas_visualization():
    diplomas = Diploma.query.all()
    return render_template('diplomas/diplomas-visualization.html', diplomas=diplomas)


@diplomas_bp.route('/view_diploma/<int:diploma_id>', methods=['GET'])
@login_required
def view_diploma(diploma_id):
    # Buscar el diploma por su ID
    diploma = Diploma.query.get(diploma_id)
    if not diploma:
        flash("Diploma   not found.", "error")
        return redirect(url_for('diplomas.diplomas_visualization'))

    # Construir la ruta al archivo PDF
    file_path = os.path.abspath(diploma.file_path)
    
    # Verificar si el archivo existe
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    else:
        flash("Diploma file not found.", "error")
        return redirect(url_for('diplomas.diplomas_visualization'))
    

@diplomas_bp.route('/delete_diploma/<int:diploma_id>', methods=['POST'])
@login_required
def delete_diploma(diploma_id):
    if request.form.get('_method') == 'DELETE':
        try:
            # Obtener el diploma por su ID
            diploma = Diploma.query.get(diploma_id)
            if diploma:
                # Generar la ruta completa del archivo PDF basado en el uvus
                file_path = os.path.abspath(diploma.file_path)
                
                # Eliminar el archivo PDF si existe
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                    except Exception as file_error:
                        flash("The diploma entry was deleted, but the file could not be deleted.", "warning")
                        print(f"Error deleting file: {file_error}")
                
                # Eliminar el registro del diploma de la base de datos
                db.session.delete(diploma)
                db.session.commit()
                flash("Diploma deleted successfully.", "success")
            else:
                flash("Diploma not found.", "error")
        except Exception as e:
            print(f"Error deleting diploma: {e}")
            flash(f"Error deleting diploma: {e}", "error")
    return redirect(url_for("diplomas.diplomas_visualization"))


@diplomas_bp.route('/send_diplomas', methods=['POST'])
@login_required
def send_diplomas():
    data = request.get_json()
    selected_ids = data.get('diploma_ids', [])

    if not selected_ids:
        return jsonify({'success': False, 'message': 'Please select at least one diploma.'})

    # Filtrar los diplomas seleccionados
    diplomas = Diploma.query.filter(Diploma.id.in_(selected_ids)).all()
    sent_count = 0

    for diploma in diplomas:
        file_path = os.path.join(current_app.root_path, "../docs", "diplomas", os.path.basename(diploma.file_path))
        if file_path and os.path.exists(file_path):
            try:
                mail_service.send_email_with_attachment(
                    subject="Your Diploma from Innosoft",
                    recipients=[diploma.correo],
                    body="Congratulations! Here is your diploma for participating in the InnoSoft Days.",
                    attachment_path_pdf=file_path
                )
                diploma.sent = True
                sent_count += 1
            except Exception as e:
                print(f"Error sending email to {diploma.correo}: {e}")
                return jsonify({'success': False, 'message': f"Failed to send email to {diploma.nombre}"})

    db.session.commit()
    return jsonify({'success': True, 'message': f"Successfully sent {sent_count} diplomas."})


@diplomas_bp.route('/manage-templates', methods=['GET', 'POST'])
@login_required
def manage_templates():
    form = UploadTemplateForm()
    templates_dir = os.path.join('docs', 'plantillas')
    
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    if form.validate_on_submit():
        pdf_file = form.pdf_file.data
        custom_text = form.custom_text.data
        
        # Validar el tipo de archivo
        if not pdf_file.filename.lower().endswith('.pdf'):
            flash("Error: Solo se permiten archivos PDF", "error")
            return redirect(url_for('diplomas.manage_templates'))

        if pdf_file:
            filename = pdf_file.filename
            save_path = os.path.join(templates_dir, filename)

            try:
                pdf_file.save(save_path)
                relative_path = os.path.join('docs', 'plantillas', filename)
                template = DiplomaTemplate(filename=filename, custom_text=custom_text, file_path=relative_path)
                db.session.add(template)
                db.session.commit()
                flash("Plantilla subida con éxito", "success")
            except Exception as e:
                flash(f"Error al guardar la plantilla: {str(e)}", "error")
    
    templates = DiplomaTemplate.query.all()
    return render_template('diplomas/manage-templates.html', form=form, templates=templates)



@diplomas_bp.route('/view_template/<int:template_id>', methods=['GET'])
@login_required
def view_template(template_id):
    template = DiplomaTemplate.query.get(template_id)
    if not template:
        flash("Plantilla no encontrada", "error")
        return redirect(url_for('diplomas.manage_templates'))
    file_path = os.path.abspath(template.file_path)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    else:
        flash("Archivo no encontrado", "error")
        return redirect(url_for('diplomas.manage_templates'))


@diplomas_bp.route('/delete_template/<int:template_id>', methods=['POST'])
@login_required
def delete_template(template_id):
    template = DiplomaTemplate.query.get(template_id)
    if template:
        file_path = os.path.abspath(template.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        db.session.delete(template)
        db.session.commit()
        flash("Plantilla eliminada con éxito", "success")
    else:
        flash("Plantilla no encontrada", "error")
    return redirect(url_for('diplomas.manage_templates'))
