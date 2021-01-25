from app import app
from app.api import select_all_records


@app.route('/')
def index() -> str:
    return select_all_records()
