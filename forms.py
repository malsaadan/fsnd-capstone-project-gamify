from flask_wtf import Form
from wtforms import StringField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, AnyOf, URL, Length
import json


class GameForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    age_rating = SelectField(
        'age_rating', validators=[DataRequired()],
        choices=[
            ('+3'),
            ('+7'),
            ('+12'),
            ('+16'),
            ('+18')
        ]
    )

    category = SelectField(
        'Category', validators=[DataRequired()]
    )

    developer = SelectField(
        'developer', validators=[DataRequired()]
    )

    image_link = StringField(
        'image_link', validators=[URL()]
    )


class CategoryForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    description = StringField(
        'description', validators=[DataRequired()]
    )


class DeveloperForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    website = StringField(
        'website', validators=[URL()]
    )
