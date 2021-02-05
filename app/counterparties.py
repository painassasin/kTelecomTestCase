import pandas as pd

from app import app
from app.DBcm import UseDatabase, ConnectionError, CredentialsError, SyntaxError


def get_records() -> dict:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = """
                SELECT
                    t.id, t.name, dct.type, vip, dl.locality, dst.service,
                    t.vlan_address_from, t.vlan_address_to,
                    CONCAT(chw.width,' ', chw.units) channel_width, 
                    DATE_FORMAT(date_of_request, '%d-%m-%Y') date_of_request,
                    dsi.description information_source, 
                    CONCAT(dm.surname,' ', dm.name) responsible_manager
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
            records = cursor.fetchall()
            df = pd.DataFrame(records, columns=cursor.column_names)
            return df.T.to_dict()
    except (ConnectionError, CredentialsError):
        return dict()


def delete_record(row_id: int) -> bool:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                DELETE FROM counterparties t
                WHERE t.id = {row_id}
            """
            cursor.execute(_SQL)
            print(f'Row #{row_id} successfully deleted')
            return True
    except (ConnectionError, CredentialsError, SyntaxError):
        return False
    except Exception as err:
        print(err)
        return False


def get_row(row_id: int) -> dict:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                SELECT 
                    t.id, t.name, t.type, t.vip, dl.locality, t.service_type,
                    t.vlan_address_from, t.vlan_address_to, 
                    t.channel_width, t.date_of_request,
                    dsi.description information_source, t.responsible_manager
                FROM counterparties t
                LEFT JOIN d_locality dl ON t.locality = dl.id
                LEFT JOIN d_source_of_information dsi 
                    ON t.information_source = dsi.id
                WHERE t.id={row_id}
            """
            cursor.execute(_SQL)
            data = cursor.fetchall()
            if data:
                return dict(zip(cursor.column_names, data[0]))
    except (ConnectionError, CredentialsError):
        return dict()


def update_record(row_id: int, form_data: dict) -> bool:
    form_data.update({
        'vip': int(form_data['vip']),
        'locality': _get_locality_id(form_data['locality']),
        'information_source': _get_source_id(form_data['information_source']),
    })
    form_data.pop('submit')
    form_data.pop('csrf_token')
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
                UPDATE counterparties
                SET {', '.join(f"{k}='{form_data[k]}'" for k in form_data)}
                WHERE id = {row_id}
            """
            cursor.execute(_SQL)
            return True
    except (ConnectionError, CredentialsError, SyntaxError) as err:
        print(err)
        return False


def _get_locality_id(locality: str) -> int:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL_INSERT = f"""
                INSERT IGNORE INTO d_locality(locality)
                VALUES('{locality}')
            """
            _SQL_SELECT = f"""
                SELECT dl.id FROM d_locality dl
                WHERE dl.locality='{locality}' LIMIT 1
            """
            cursor.execute(_SQL_INSERT)
            cursor.execute(_SQL_SELECT)
            locality_id = cursor.fetchone()
            if locality_id:
                return locality_id[0]
    except (ConnectionError, CredentialsError) as err:
        print(err)


def _get_source_id(description: str) -> int:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL_INSERT = f"""
                INSERT IGNORE INTO d_source_of_information(description) 
                VALUES('{description}');
            """
            _SQL_SELECT = f"""
                SELECT dsi.id FROM d_source_of_information dsi
                WHERE dsi.description='{description}' LIMIT 1
            """
            cursor.execute(_SQL_INSERT)
            cursor.execute(_SQL_SELECT)
            source_id = cursor.fetchone()
            if source_id:
                return source_id[0]
    except (ConnectionError, CredentialsError) as err:
        print(err)
