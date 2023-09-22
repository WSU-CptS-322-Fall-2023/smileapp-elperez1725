from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import  DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

from app.Model.models import Post, Tag

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
    body = TextAreaField('Body', validators=[DataRequired(), Length(min=1, max=1500)])
    tag =  QuerySelectMultipleField( 'Tag', query_factory=lambda: Tag.query.all(), get_label=lambda tag: tag.name, widget=ListWidget(prefix_label=False), 
        option_widget=CheckboxInput() )
    submit = SubmitField('Post')


class SortForm(FlaskForm):
    sort_by = SelectField('Sort By', choices=[
        ('date', 'Date'), 
        ('title', 'Title'), 
        ('likes', '# of likes'), 
        ('happiness', 'Happiness level')])
    refresh = SubmitField('Refresh')
   
