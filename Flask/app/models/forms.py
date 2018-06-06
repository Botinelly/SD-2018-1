from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, RadioField, IntegerField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])

#INSERT INTO users (username, password,admin ) VALUES ("lucas.botinelly", "paocommanteiga", 1)

class CallForm(FlaskForm):
    user = StringField("user", validators = [DataRequired()])
    category = StringField("category", validators = [DataRequired()])
    subcategory = StringField("subcategory", validators = [DataRequired()])
    reward = StringField("reward", validators = [DataRequired()])
    obs = TextAreaField("obs", validators= [DataRequired()])

class EditForm(FlaskForm):
    options = RadioField("options", choices = [(3, "Concluído"),(2, "Visualizado"),(1, "Não Atendido")], validators = [DataRequired()])
    form_id = IntegerField("id", validators = [DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField("username", validators = [DataRequired()])
    password = PasswordField("password", validators = [DataRequired()])
    password2 = PasswordField("password2", validators = [DataRequired()])

class AvlForm(FlaskForm):
    nota = RadioField("Nota do Chamado :", choices = [(1, "Péssimo"),(2, "Ruim"),(3, "Normal"),(4, "Bom"),(5, "Ótimo")])
    form_id = IntegerField("id", validators = [DataRequired()])

class DeleteForm(FlaskForm):
    id = IntegerField("id", validators = [DataRequired()])

class UpdateForm(FlaskForm):
    form_id = IntegerField("id", validators = [DataRequired()])
    nova_senha = PasswordField("password", validators = [DataRequired()])
    nova_senha2 = PasswordField("password2", validators = [DataRequired()])
