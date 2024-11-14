from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

# Formulário de Status
class StatusForm(FlaskForm):
    statusDescricao = StringField('Descrição do Status', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Salvar')