import os
from os import path
from flask import Flask, render_template, url_for, request, flash, current_app, redirect, session
from flask_bootstrap import Bootstrap
from flask_wtf import Form, FlaskForm
from flask_mail import Message, Mail
from wtforms import SubmitField, SelectField, ValidationError, StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import InputRequired, Email, DataRequired, Length, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bootstrap = Bootstrap(app)


DEBUG=True
Basedir = path.abspath(path.dirname(__file__))
MusicFolder = os.path.join(Basedir, 'static/mp3')
UploadFolder = 'uploads'

app.config['MusicFolder'] = MusicFolder
app.config['UploadFolder'] = UploadFolder
app.config.from_object(__name__)
app.config['SECRET_KEY']='123456789_ABC'
db_path = os.path.join(os.path.dirname(__file__), 'database/books.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db_path_2 = os.path.join(os.path.dirname(__file__), 'database/shelves.db')
db_uri_2 = 'sqlite:///{}'.format(db_path_2)
app.config['SQLALCHEMY_BINDS']= {'shelves': db_uri_2}
app.config['CSRF_ENABLED']= True

db=SQLAlchemy(app)
# db.create_all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30))
    Date = db.Column(db.String(40))
    FinishReading = db.Column(db.String(30))
    Author = db.Column(db.String(30))
    Shelfname = db.Column(db.String(30))


class Shelf(db.Model):
    __bind_key__='shelves'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(30))

class BookForm(FlaskForm):
    Name = StringField('Book', validators=[InputRequired(), Length(min=1, max=30)])
    Date = StringField('Date', validators=[InputRequired(), Length(min=1, max=30)])
    Author = StringField('Author', validators=[InputRequired(), Length(min=1, max=30)])
    Shelfname = StringField('Shelf', validators=[Length(min=0, max=30)])
    FinishReading = RadioField('Did you read the book?', choices = [('Not Reading','Not read yet'), ('Reading','reading'), ('Finished reading','finished reading')], validators=[InputRequired()])


class ShelfForm(FlaskForm):
    Name = StringField('Shelf Name', validators=[InputRequired(), Length(min=1, max=30)])



@app.route('/')
def Welcome():
    #check if Shlef has a shlef named 'reading'
    if not Shelf.query.filter_by(Name='Reading').first():
        shelf = Shelf(Name='Reading')
        shelf2 = Shelf(Name='Not Reading')
        shelf3 = Shelf(Name='Finished reading')
        db.session.add(shelf)
        db.session.add(shelf2)
        db.session.add(shelf3)
        db.session.commit()
    return redirect('/Home')

@app.route('/Home')
def Home():
    # Songs =  Song.query.all()
    # return render_template('Home.html', Songs=Songs)
    Books = Book.query.all()
    Shelves = Shelf.query.all()
    return render_template('Home.html', Books=Books, Shelves=Shelves)

@app.route('/AddBook', methods=['GET', 'POST'])
def AddBook():
    form = BookForm()

    if form.validate_on_submit():
        new_book = Book(Name=form.Name.data, Date=form.Date.data, Author=form.Author.data, Shelfname=form.Shelfname.data, FinishReading=form.FinishReading.data)
        db.session.add(new_book)
        db.session.commit()
        return render_template('DynamicTable.html', form=form, success= True)

    return render_template('DynamicTable.html', form=form)

@app.route('/AddShelf', methods=['GET', 'POST'])
def AddShelf():
    form = ShelfForm()

    if form.validate_on_submit():
        new_shlef = Shelf(Name=form.Name.data)
        db.session.add(new_shlef)
        db.session.commit()
        return render_template('AddShelf.html', form=form, success= True)

    return render_template('AddShelf.html', form=form)

# -------------------Update-------------------
@app.route('/Update/<int:id>', methods=['GET', 'POST'])
def UpdateBook(id):
    book = Book.query.get_or_404(id)

    if request.method == 'POST':
        book.Name = request.form['name']
        book.Date = request.form['date']
        book.Author = request.form['author']
        book.Shelfname = request.form['shelfname']
        book.FinishReading = request.form['finishreading']
        try:
            db.session.commit()
            return redirect('/Home')
        except:
            return 'There was an issue updating your book'
    else:
        return render_template('updateBook.html', book=book)

@app.route('/UpdateShelf/<int:id>', methods=['GET', 'POST'])
def UpdateShelf(id):
    shelf = Shelf.query.get_or_404(id)

    if request.method == 'POST':
        shelf.Name = request.form['name']
    

        try:
            db.session.commit()
            return redirect('/Home')
        except:
            return 'There was an issue updating your shelf'
    else:
        return render_template('updateShelf.html', shelf=shelf)



@app.route('/DisplayShelf/<name>', methods=['GET'])
def DisplayShelf(name):
    Books = Book.query.all()
    if(name == 'Reading' or name=='Not Reading' or name=='Finished reading'):
        return render_template('DisplayDefault3shelves.html', Books=Books, name=name)
    else:
        return render_template('DisplayShelf.html', Books=Books, name = name)

# update Book
@app.route('/AddBookDefault', methods=['GET', 'POST'])
def AddBookDefault():
    new_book = Book(Name= "Default", Date = "DefaultDate")
    db.session.add(new_book)
    db.session.commit()
    Books = Book.query.all()

    return render_template('Home.html', Books=Books)



with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(host='0.0.0.0',port=8000,debug=True)
