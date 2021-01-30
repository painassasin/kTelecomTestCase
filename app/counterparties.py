from app.DBcm import UseDatabase
from app.DBcm import ConnectionError, CredentialsError, DuplicationError, SyntaxError
from app import app
import pandas as pd


class Counterparties:
    def __init__(self):
        self.table_name = 'counterparties'

    @staticmethod
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

    def _get_column_names(self) -> list:
        try:
            with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
                _SQL = f'SHOW COLUMNS FROM {self.table_name}'
                cursor.execute(_SQL)
                return [i[0] for i in cursor.fetchall()]
        except (ConnectionError, CredentialsError):
            return []

    def to_dict(self) -> dict:
        columns = self._get_column_names()
        records = self._select_all_records()
        df = pd.DataFrame(records, columns=columns)
        return df.T.to_dict()

    @staticmethod
    def delete_row(row_id: int) -> bool:
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

