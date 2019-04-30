# the registration form to allow us to register new users
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField        #We add a BooleanField input field that will render a checkbox in our form.
from wtforms.validators import Required,Email,EqualTo   #the EqualTo  helps us in comparing the two password inputs.
from ..models import User
from wtforms import ValidationError


class RegistrationForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')

    def validate_email(self,data_field):
            if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')

    def validate_username(self,data_field):                                       #validate_username checks to see if the username is unique and raises a ValidationError if another user with a similar username is found.
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('That username is taken')



class LoginForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    password = PasswordField('Password',validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')
