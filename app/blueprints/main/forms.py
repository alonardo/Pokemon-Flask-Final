from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class PokemonForm(FlaskForm):
    poke_name = StringField("Pokemon Name", validators=[DataRequired()])

    