from flask_wtf import FlaskForm
from wtforms import SelectField, BooleanField, StringField, TextAreaField
from wtforms import DateField, SubmitField


class EditCounterpartiesForm(FlaskForm):
    cp_name = StringField(label='Наименование контрагента')
    cp_type = SelectField(label='Тип контрагента')
    cp_vip = BooleanField(label='VIP клиент')
    cp_location = StringField(label='Населенный пункт')
    cp_service_type = SelectField(label='Тип услуги')
    cp_vlan_address_from = TextAreaField(label='Адес VLAN от',
                                         description='Город, улица, дом')
    cp_vlan_address_to = TextAreaField(label='Адес VLAN до',
                                       description='Город, улица, дом')
    cp_channel_width = SelectField(label='Ширина канала')
    cp_request_date = DateField(label='Дата заявки')
    cp_information_source = TextAreaField(label='От куда узнали об услугах')
    cp_responsible_manager = SelectField(label='Ответственный менеджер')
    submit = SubmitField(label='Изменить')





