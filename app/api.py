from app.DBcm import UseDatabase
from app import app


def select_all_records() -> dict:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = """
                SELECT
                    id, name, type, vip, locality, service_type, vlan_address_from, vlan_address_to,
                    channel_width, date_of_request, information_source, responsible_manager
                FROM
                    counterparties
                    """
            cursor.execute(_SQL)
            return {'data': cursor.fetchall()}
    except Exception as err:
        return {'error': err}
