from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo, Length, NumberRange
from app.models import Usuario, Status, Fazenda, UsuariosPerfis, Menu, MiniApp, PerfisPermissoes
from wtforms_sqlalchemy.fields import QuerySelectField

class StatusForm(FlaskForm):
    statusDescricao = StringField('Descrição do Status', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Salvar')

    def validate_statusDescricao(self, statusDescricao):
        status = Status.query.filter_by(statusDescricao=statusDescricao.data).first()
        if status:
            raise ValidationError('Já existe um status com essa descrição.')

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

class UsuariosPerfisForm(FlaskForm):
    perfilNome = StringField('Nome do Perfil', validators=[DataRequired(), Length(max=50)])
    perfilDescricao = StringField('Descrição do Perfil', validators=[Length(max=100)])
    statusId = SelectField('Status', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

class UsuarioForm(FlaskForm):
    usuarioNome = StringField('Nome', validators=[DataRequired(), Length(max=150)])
    usuarioEmail = StringField('E-mail', validators=[DataRequired(), Email()])
    usuarioSenha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=50)])
    confirmarSenha = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('usuarioSenha', message='As senhas devem coincidir.')
    ])
    usuarioDataValidadePermissao = DateTimeField('Validade da Permissão', format='%Y-%m-%d', validators=[DataRequired()])
    statusId = SelectField('Status', choices=[], coerce=int, validators=[DataRequired()])
    fazendaId = SelectField('Fazenda', choices=[], coerce=int)
    usuarioPerfilId = SelectField('Perfil', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

    def __init__(self, usuario_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario_id = usuario_id

    def validate_usuarioEmail(self, usuarioEmail):
        usuario = Usuario.query.filter_by(usuarioEmail=usuarioEmail.data).first()
        if usuario and usuario.usuarioId != self.usuario_id:
            raise ValidationError('Já existe um usuário com este e-mail.')

class MenuForm(FlaskForm):
    menuNome = StringField(
        "Nome do Menu",
        validators=[DataRequired(), Length(max=30)],
    )
    menuOrdem = IntegerField(
        "Ordem do Menu",
        validators=[DataRequired()],
    )
    menuTemplate = StringField(
        "Template do Menu",
        validators=[DataRequired(), Length(max=50)],
    )
    submit = SubmitField("Salvar")

    def validate_menuNome(self, field):
        existing_menu = Menu.query.filter_by(menuNome=field.data).first()
        if existing_menu:
            raise ValidationError("Já existe um menu com esse nome.")

    def validate_menuTemplate(self, field):
        existing_template = Menu.query.filter_by(menuTemplate=field.data).first()
        if existing_template:
            raise ValidationError("Já existe um template com esse nome.")

class MiniAppForm(FlaskForm):
    miniAppNome = StringField("Nome do MiniApp", validators=[DataRequired()])
    miniAppIcon = StringField("Ícone do MiniApp", validators=[DataRequired()])
    miniAppLink = StringField("Link do MiniApp", validators=[DataRequired()])
    menuId = QuerySelectField(
        "Menu",
        query_factory=lambda: Menu.query.order_by(Menu.menuNome).all(),
        get_label="menuNome",
        allow_blank=False,
        validators=[DataRequired()]
    )
    submit = SubmitField("Salvar")

class PerfisPermissoesForm(FlaskForm):
    perfilId = SelectField('Perfil', choices=[], coerce=int, validators=[DataRequired()])
    miniAppId = SelectField('MiniApp', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Salvar')

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")

class UsuariosPermissoesForm(FlaskForm):
    usuarioId = SelectField('Usuário', choices=[], coerce=int, validators=[DataRequired()])
    miniAppId = SelectField('MiniApp', choices=[], coerce=int, validators=[DataRequired()])
    statusId = SelectField('Status', choices=[], coerce=int, validators=[DataRequired()])
    permissaoMotivo = StringField('Motivo da Permissão', validators=[Length(max=255)])
    submit = SubmitField('Salvar')

class EscolhaTemaForm(FlaskForm):
    preferenciaTema = SelectField(
        'Escolha o Tema',
        choices=[
            ('Default', 'Default'),
            ('Dark', 'Dark'),
            ('Light', 'Light'),
            ('Custom', 'Custom')
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField('Salvar')

from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired

class EscolherMiniAppsHomeForm(FlaskForm):
    miniapps = SelectMultipleField(
        'MiniApps',
        coerce=int,
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        validators=[DataRequired()]
    )
    submit = SubmitField('Salvar Preferências')
