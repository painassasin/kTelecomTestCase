from app import app
from app.counterparties import values_to_dict, delete_record, get_managers
from app.counterparties import get_types, get_service_types, get_channel_width
from flask import render_template, request, jsonify
from app.forms import EditCounterpartiesForm


@app.route('/')
def index():
    table_dict = values_to_dict()
    return render_template('index.html', table=table_dict.values())


@app.route('/delete-row', methods=['POST'])
def delete_row():
    success = False
    if request.is_json:
        row_id = request.get_json().get('id')
        success = delete_record(row_id)
    return jsonify({'success': success})


@app.route('/update')
def update_row():
    form = EditCounterpartiesForm()
    form.cp_type.choices = get_types()
    form.cp_service_type.choices = get_service_types()
    form.cp_channel_width.choices = get_channel_width()
    form.cp_responsible_manager.choices = get_managers()
    return render_template('edit_row.html', form=form)

