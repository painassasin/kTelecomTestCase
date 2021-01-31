from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, StringField, TextAreaField
from wtforms import DateField, SubmitField
from app import app
from app.DBcm import UseDatabase
from app.DBcm import ConnectionError, CredentialsError


def get_types() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = 'SELECT * FROM d_counterparty_type t'
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_service_types() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = 'SELECT * FROM d_service_type t'
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


def get_channel_width() -> list:
    try:
        with UseDatabase(app.config['DB_CREDENTIALS']) as cursor:
            _SQL = """
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
            _SQL = """
                SELECT t.id, CONCAT(t.surname, ' ', t.name) manager
                FROM d_managers t
            """
            cursor.execute(_SQL)
            return cursor.fetchall()
    except (ConnectionError, CredentialsError):
        return []


class EditCounterpartiesForm(FlaskForm):
    name = StringField(label='Наименование контрагента',
                       render_kw={'class': 'form-control'})
    type = SelectField(label='Тип контрагента',
                       coerce=int,
                       choices=get_types(),
                       render_kw={'class': 'custom-select'})
    vip = BooleanField(label='VIP клиент',
                       render_kw={'class': 'form-check-input'})
    locality = StringField(label='Населенный пункт',
                           render_kw={'class': 'form-control'})
    service_type = SelectField(label='Тип услуги',
                               coerce=int,
                               choices=get_service_types(),
                               render_kw={'class': 'custom-select'})
    vlan_address_from = TextAreaField(label='Адес VLAN от',
                                      render_kw={
                                          'class': 'form-control',
                                          'rows': 2,
                                          'placeholder': 'Город, улица, дом'})
    vlan_address_to = TextAreaField(label='Адес VLAN до',
                                    render_kw={
                                        'class': 'form-control',
                                        'rows': 2,
                                        'placeholder': 'Город, улица, дом'})
    channel_width = SelectField(label='Ширина канала',
                                coerce=int,
                                choices=get_channel_width(),
                                render_kw={'class': 'custom-select'})
    date_of_request = DateField(label='Дата заявки',
                                render_kw={
                                    'class': 'form-control',
                                    'type': 'date'})
    information_source = TextAreaField(label='От куда узнали об услугах',
                                       render_kw={
                                           'class': 'form-control',
                                           'rows': 2})
    responsible_manager = SelectField(label='Ответственный менеджер',
                                      coerce=int,
                                      choices=get_managers(),
                                      render_kw={'class': 'custom-select'})
    submit = SubmitField(label='Изменить',
                         render_kw={'class': 'btn btn-primary btn-block'})
