from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import Usuario
from app import db, bcrypt

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(usuarioEmail=form.email.data).first()
        if user and bcrypt.check_password_hash(user.usuarioSenha, form.password.data):
            login_user(user, remember=True)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("main_bp.home"))
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("auth.login"))
