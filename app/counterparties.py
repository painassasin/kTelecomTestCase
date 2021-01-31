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


def update_row_data(row_id: int, form_data: dict) -> bool:
    form_data.update({
        'vip': int(form_data['vip']),
        'locality': _get_locality_id(form_data['locality']),
        'information_source': _get_source_id(form_data['information_source']),
    })
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = f"""
            UPDATE counterparties t
            SET
                name='{form_data['name']}', 
                type='{form_data['type']}',
                vip='{form_data['vip']}',
                locality='{form_data['locality']}',
                service_type='{form_data['service_type']}',
                vlan_address_from='{form_data['vlan_address_from']}',
                vlan_address_to='{form_data['vlan_address_to']}',
                channel_width='{form_data['channel_width']}',
                date_of_request='{form_data['date_of_request']}',
                information_source='{form_data['information_source']}',
                responsible_manager='{form_data['responsible_manager']}'
            WHERE t.id={row_id}
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




