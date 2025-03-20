from flask_wtf import FlaskForm
from wtforms import (StringField, FloatField, SelectField, 
                    BooleanField, PasswordField, SubmitField)
from wtforms.validators import DataRequired, Email, NumberRange, ValidationError
from app.models import User

class PRPForm(FlaskForm):
    basic = FloatField('Basic Pay (₹)', 
                      validators=[
                          DataRequired(),
                          NumberRange(min=0, message="Value must be positive")
                      ])
    
    da = FloatField('Dearness Allowance (₹)', 
                   validators=[
                       DataRequired(),
                       NumberRange(min=0)
                   ])
    
    company_rating = SelectField('Company Rating',
                                choices=[
                                    ('Good', 'Good (1.0x)'),
                                    ('Very Good', 'Very Good (1.2x)'),
                                    ('Excellent', 'Excellent (1.5x)')
                                ],
                                validators=[DataRequired()])
    
    individual_rating = SelectField('Individual Performance',
                                   choices=[
                                       (1, '1 - Needs Improvement (0.0x)'),
                                       (2, '2 - Average (0.5x)'), 
                                       (3, '3 - Good (1.0x)'),
                                       (4, '4 - Very Good (1.3x)'),
                                       (5, '5 - Outstanding (1.5x)')
                                   ],
                                   coerce=int,
                                   validators=[DataRequired()])
    
    employee_type = SelectField('Employee Category',
                               choices=[
                                   ('Executive', 'Executive (50% Cap)'),
                                   ('Non-Executive', 'Non-Executive (30% Cap)')
                               ],
                               validators=[DataRequired()])
    
    profit_met = SelectField('Profit Target Achieved?',
                            choices=[
                                (True, 'Yes'),
                                (False, 'No')
                            ],
                            coerce=bool,
                            validators=[DataRequired()])
    
    include_tax = BooleanField('Include Tax Impact')
    include_projections = BooleanField('5-Year Projections')
    
    submit = SubmitField('Calculate PRP')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    employee_id = StringField('Employee ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                    validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')