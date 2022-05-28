from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField,StringField,PasswordField
from wtforms.validators import DataRequired, EqualTo,  ValidationError
from app.models import User

class RegistForm(FlaskForm):

    name = StringField(
        label="Name",
        validators=[
            DataRequired("Please input your password")
        ],
        description="Name",
        render_kw={
            "class":"form-control input-lg",
            "placeholder":"please input your password here！"
        }
    )

    pwd = PasswordField(
        label="Password",
        validators=[
            DataRequired("Please enter your password")
        ],
        description="Password",
        render_kw={
            "class":"form-control input-lg",
            "placeholder": "Please enter your password"
        }
    )
    repwd = PasswordField(
        label="Repeat password",
        validators=[
            DataRequired("Please enter your password!"),
            EqualTo('pwd',message="Two password is not the same")
        ],
        description="Repeat password",
        render_kw={
            "class":"form-control input-lg",
            "placeholder": "Please input the password again"
        }
    )

    submit = SubmitField(
        label="Sumbit to register",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

    def validate_name(self,field):
        name=field.data
        user=User.query.filter_by(name=name).count()
        if user==1:
            raise ValidationError("Username already exsists！")


class LoginForm(FlaskForm):

    name = StringField(
        label="Username",
        validators=[
            DataRequired("Please input your user name")
        ],
        description="Username",
        render_kw={

            "class":"form-control input-lg",
            "placeholder":"Please input your username"
        }
    )

    pwd = PasswordField(
        label="Password",
        validators=[
            DataRequired("Please enter your password!")
        ],
        description="Password",
        render_kw={
            "class":"form-control input-lg",
            "placeholder": "Please enter your password！"
        }
    )

    submit = SubmitField(
        label="Login",
        render_kw={
            "class": "btn btn-lg btn-success btn-block"
        }
    )

class PostForm(FlaskForm):
    input_lexical = CKEditorField('input_lexical')
    input_syntactic = CKEditorField('input_syntactic')
    submit = SubmitField('submit')

