from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)


app.config['SECRET_KEY'] = "JSTANTAKENDRICK"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:10854@localhost/quotes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kbxwtiadbayjcg:1c821a2d89bcb69d65c4564bc9ab243a617a8e6e3387b7d9fe3bdaa6b97235f8@ec2-34-232-191-133.compute-1.amazonaws.com:5432/da8t9fshre9fsj'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)

# Create a Form class
class QuoteForm(FlaskForm):
    author = StringField("Author Name", validators=[DataRequired()])
    quote = TextAreaField("Quote message", validators=[DataRequired()])
    submit = SubmitField("Submit")


class Favquote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    quote = db.Column(db.String(2000))


@app.route('/')
def index():
    result = Favquote.query.all()
    return render_template('index.html', result=result)


@app.route('/quotes')
def quotes():
    author = None
    quote = None
    form = QuoteForm()
    if form.validate_on_submit():
        author = form.author.data
        form.author.data = ''
        quote = form.quote.data
        form.quote.data = ''
    return render_template('quotes.html', form=form)


@app.route('/process', methods=['POST'])
def process():
    author = request.form['author']
    quote = request.form['quote']
    quotedata = Favquote(author=author, quote=quote)
    db.session.add(quotedata)
    db.session.commit()
    return redirect(url_for('index'))
