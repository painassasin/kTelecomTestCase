from app import app
from app.actions import Counterparties
from flask import render_template


@app.route('/')
def index() -> str:
    table = Counterparties()
    table_dict = table.to_dict()
    return render_template('view.html', table=table_dict.values())
