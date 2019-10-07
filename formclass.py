from flask import Flask, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired, Length

class newuser(Form):
    name = TextField('Name:', validators=[DataRequired(), Length(min=2, max=20)])

class newgroup(Form):
    name = TextField('Name:', validators=[DataRequired(), Length(min=2, max=20)])
