from flask import Flask, render_template, request, redirect, url_for, flash
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from utils.email_utils import fetch_and_process_emails

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/emailDB'
mongo = PyMongo(app)

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    keywords = StringField('Keywords (comma separated)', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = EmailForm()
    if request.method == 'POST':
        print("Form Gönderildi")
        if form.validate_on_submit():
            print("Form Geçerli")
            email = form.email.data
            password = form.password.data
            keywords = form.keywords.data.split(',')
            result = fetch_and_process_emails(email, password, keywords, mongo)
            flash(result)
            return redirect(url_for('index'))
        else:
            print("Form Geçerli Değil")
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
