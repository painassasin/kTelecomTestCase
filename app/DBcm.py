import mysql.connector


class UseDatabase:

    def __init__(self, config:dict) -> None:
        self.configuration = config

    def __enter__(self) -> mysql.connector.cursor:
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except Exception as err:
            raise Exception(err)

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

