import mysql.connector


class CredentialsError(Exception):
    pass


class DuplicationError(Exception):
    pass


class ConnectionError(Exception):
    pass


class SyntaxError(Exception):
    pass


class UseDatabase:

    def __init__(self, config: dict) -> None:
        self.config = config

    def __enter__(self) -> mysql.connector.cursor:
        try:
            self.conn = mysql.connector.connect(**self.config, use_unicode=True, charset='utf8')
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.ProgrammingError as e:
            if e.args[0] == 1045:
                raise CredentialsError(e)
            if e.args[0] == 1064:
                raise SyntaxError(e)
        except mysql.connector.errors.IntegrityError as e:
            raise DuplicationError(e)
        except mysql.connector.errors.DatabaseError as e:
            raise ConnectionError(e)

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type == mysql.connector.errors.ProgrammingError:
            raise SyntaxError(exc_value)
