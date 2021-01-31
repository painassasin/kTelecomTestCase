from app.DBcm import UseDatabase
from app.DBcm import ConnectionError, CredentialsError, DuplicationError, SyntaxError
from app import app
import pandas as pd


def _get_column_names() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f'SHOW COLUMNS FROM counterparties'
            cursor.execute(_SQL)
            return [i[0] for i in cursor.fetchall()]
    except (ConnectionError, CredentialsError):
        return []


def _select_all_records() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = """
                SELECT
                    t.id, t.name, dct.type, vip, dl.locality, dst.service,
                    t.vlan_address_from, t.vlan_address_to,
                    CONCAT(chw.width,' ', chw.units), 
                    DATE_FORMAT(date_of_request, '%d-%m-%Y'),
                    dsi.description, CONCAT(dm.surname,' ', dm.name)
                FROM
                    counterparties t
                LEFT JOIN d_counterparty_type dct ON t.type = dct.id
                LEFT JOIN d_locality dl ON t.locality = dl.id
                LEFT JOIN d_service_type dst ON t.service_type = dst.id
                LEFT JOIN d_channel_width chw ON t.channel_width = chw.id
                LEFT JOIN d_source_of_information dsi 
                    ON t.information_source = dsi.id
                LEFT JOIN d_managers dm ON t.responsible_manager = dm.id
                    """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def values_to_dict() -> dict:
    columns = _get_column_names()
    records = _select_all_records()
    df = pd.DataFrame(records, columns=columns)
    return df.T.to_dict()


def delete_record(row_id: int) -> bool:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                DELETE FROM counterparties t
                WHERE t.id = {row_id}
            """
            cursor.execute(_SQL)
            return True
    except (ConnectionError, CredentialsError, SyntaxError):
        return False
    except Exception as err:
        print(err)
        return False


def get_types() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT t.id, t.type
                FROM d_counterparty_type t
            """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_service_types() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT t.id, t.service
                FROM d_service_type t
            """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_channel_width() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT t.id, CONCAT(t.width, ' ', t.units) width
                FROM d_channel_width t
            """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_managers() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT t.id, CONCAT(t.surname, ' ', t.name) manager
                FROM d_managers t
            """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_row(row_id: int) -> dict:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT 
                    t.id, t.name, t.type, t.vip, dl.locality, t.service_type,
                    t.vlan_address_from, t.vlan_address_to, 
                    t.channel_width, t.date_of_request,
                    dsi.description, t.responsible_manager
                FROM counterparties t
                LEFT JOIN d_locality dl ON t.locality = dl.id
                LEFT JOIN d_source_of_information dsi 
                    ON t.information_source = dsi.id
                WHERE t.id={row_id}
            """
            cursor.execute(_SQL)
            data = cursor.fetchall()
            if data:
                return dict(zip(_get_column_names(), data[0]))
    except (ConnectionError, CredentialsError):
        return dict()
