from flask import render_template, flash, url_for, redirect, Flask, send_file
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date
from app import app, db, lm, bcrypt
import numpy as np
import pandas as pd
from io import BytesIO
from flask_bcrypt import check_password_hash, generate_password_hash

from app.models.tables import User, Post

from app.models.forms import LoginForm, CallForm, EditForm, RegisterForm, AvlForm, DeleteForm, UpdateForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index")
@login_required
def index():
    return render_template('index.html')

@app.route("/chamado", methods=["POST", "GET"])
@login_required
def chamado():
    form = CallForm()
    if form.category.data == 'None' or form.category.data == None:
        pass
    else:
        c = Post(form.category.data, form.subcategory.data, form.obs.data, form.reward.data, User.get_name(current_user), 1)
        db.session.add(c)
        db.session.commit()
        aux = Post.query.filter_by(id = c.id).first()
        flash("Chamado número " + str(aux) + " efetuado com sucesso! ")
        return redirect(url_for("index"))

    return render_template('chamado.html',  form = form)

@app.route("/lista", methods=["POST", "GET"])
@login_required
def lista():
    form = EditForm()
    teste = form.form_id.data
    upd = Post.query.filter_by(id = teste).first()

    if(upd != None):
        upd.status = form.options.data
        db.session.add(upd)
        db.session.commit()

    x = Post.query.all()
    return render_template('lista.html', post = x, form = form)

@app.route("/meuchamado", methods=["POST", "GET"])
@login_required
def meuchamado():
    form = AvlForm()
    x = Post.query.filter_by(user_id = User.get_name(current_user)).all()
    temp = form.form_id.data
    avl = Post.query.filter_by(id = temp).first()
    if(avl != None):
        avl.aval = form.nota.data
        db.session.add(avl)
        db.session.commit()
    return render_template('meu_chamado.html', post = x, form = form)

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        pwd = bcrypt.check_password_hash(user.password, form.password.data)
        if user and pwd:
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Login Inválido")

    return render_template('login.html', form = form)

@app.route("/gerencia", methods=["POST", "GET"])
@login_required
def gerencia():
    return render_template('gerencia.html')

@app.route("/update", methods=["POST", "GET"])
@login_required
def update():
    uf = UpdateForm()
    user = User.query.all()
    if uf.validate_on_submit():
        for i in user:
            if i.id == uf.form_id.data and uf.nova_senha.data == uf.nova_senha2.data:

                i.password = bcrypt.generate_password_hash(uf.nova_senha.data).decode("utf-8")
                i.password2 = i.password

                db.session.add(i)
                db.session.commit()
                flash('Senha alterada com sucesso!')
                break
            else:
                flash('Senhas não condizem !')
                break

    return render_template('update.html', uf = uf, user = user)

@app.route("/delete", methods=["POST", "GET"])
@login_required
def delete():
    df = DeleteForm()
    usr = User.query.all()
    if df.validate_on_submit():
        for i in usr:
            if i.id == current_user.user_id:
                if i.id == df.id.data and df.id.data != User.get_id(current_user):
                    p = Post.query.filter_by(user_id = i.username).all()
                    for j in p:
                        db.session.delete(j)
                    db.session.delete(i)
                    db.session.commit()
                    flash('Usuário Deletado !')
                else:
                    flash('Erro ao deletar usuário!')
            else:
                flash('Você não pode excluir este usuário !')
    return render_template('delete.html', df = df, usr = usr)

@app.route("/register", methods=["POST", "GET"])
def register():
    rf = RegisterForm()
    if rf.validate_on_submit():
        if rf.password.data == rf.password2.data:
            pw_hash = bcrypt.generate_password_hash(rf.password.data).decode("utf-8")
            user = User(rf.username.data, pw_hash)
            db.session.add(user)
            db.session.commit()
            flash('Registrado !')
            return redirect(url_for('login'))
        else:
            flash('Senhas não correspondem !')
    return render_template('register.html', rf = rf)


@app.route("/logout")
def logout():
    logout_user()
    flash("Deslogado")
    return redirect(url_for("login"))

@app.route("/teste")
def teste():
    return render_template('temp.html')
