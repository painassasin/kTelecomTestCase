from app import app
from app.counterparties import get_records, delete_record, get_row, update_record
from flask import render_template, request, jsonify, redirect, url_for
from app.forms import EditCounterpartiesForm


@app.route('/')
def index():
    records = get_records()
    return render_template('index.html', table=records.values())


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
        result = update_record(row_id, form.data)
        if result:
            return redirect(url_for('index'))
    row_data = get_row(row_id)
    if row_data:
        print(row_data)
        form = EditCounterpartiesForm(**row_data)
    return render_template('edit_row.html',
                           form=form,
                           title='Форма изменения записи')

