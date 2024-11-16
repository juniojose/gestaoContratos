from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from .models import Fazenda

# Formulário de Status
class StatusForm(FlaskForm):
    statusDescricao = StringField('Descrição do Status', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Salvar')

class FazendaForm(FlaskForm):
    fazendaSigla = StringField('Sigla', validators=[DataRequired(), Length(min=2, max=2)])
    fazendaNome = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    fazendaCEP = StringField('CEP', validators=[DataRequired(), Length(min=8, max=8)])
    fazendaEstado = StringField('Estado', validators=[DataRequired(), Length(max=50)])
    fazendaCidade = StringField('Cidade', validators=[DataRequired(), Length(max=50)])
    fazendaBairro = StringField('Bairro', validators=[Length(max=100)])
    fazendaLogradouro = StringField('Logradouro', validators=[Length(max=100)])
    fazendaNumero = StringField('Número', validators=[Length(max=6)])
    fazendaComplemento = StringField('Complemento', validators=[Length(max=50)])
    statusId = SelectField('ID do Status', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self, *args, **kwargs):
        self.fazenda_id = kwargs.pop('fazenda_id', None)
        super().__init__(*args, **kwargs)

    def validate_fazendaSigla(self, fazendaSigla):
        fazenda = Fazenda.query.filter_by(fazendaSigla=fazendaSigla.data).first()
        if fazenda and fazenda.fazendaId != self.fazenda_id:
            raise ValidationError('Já existe uma fazenda com essa sigla.')

    def validate_fazendaNome(self, fazendaNome):
        fazenda = Fazenda.query.filter_by(fazendaNome=fazendaNome.data).first()
        if fazenda and fazenda.fazendaId != self.fazenda_id:
            raise ValidationError('Já existe uma fazenda com esse nome.')