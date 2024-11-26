from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.forms import StatusForm, FazendaForm, UsuariosPerfisForm
from app.models import Status, Fazenda, UsuariosPerfis
from app import db
from sqlalchemy.exc import IntegrityError

main_bp = Blueprint('main_bp', __name__)

# Rota para login
@main_bp.route("/", methods=['GET', 'POST'])
def login():
    return redirect(url_for('main_bp.home'))

# Rota para a página inicial
@main_bp.route("/home")
def home():
    return render_template('home.html')

