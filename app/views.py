from app import app
from app.counterparties import Counterparties
from flask import render_template, request, jsonify


@app.route('/')
def index():
    table = Counterparties()
    table_dict = table.to_dict()
    return render_template('view.html', table=table_dict.values())


@app.route('/delete-row', methods=['POST'])
def delete_row():
    id = request.get_json().get('id')
    success = Counterparties.delete_row(id)
    return jsonify({'success': success})
