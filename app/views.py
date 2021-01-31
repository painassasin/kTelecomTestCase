from app import app
from app.counterparties import values_to_dict, delete_record, get_row, update_row_data
from flask import render_template, request, jsonify, redirect, url_for
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


@app.route('/update/<int:row_id>', methods=['GET', 'POST'])
def update_row(row_id):
    form = EditCounterpartiesForm()
    if form.validate_on_submit():
        update_row_data(row_id, form.data)
        # return redirect(url_for('index'))
    row_data = get_row(row_id)
    if row_data:
        form = EditCounterpartiesForm(**row_data)

    return render_template('edit_row.html', form=form)

