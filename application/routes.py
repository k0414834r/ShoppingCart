from application import app, db
from application.models import User, Post, Member
from flask import render_template, url_for, redirect, flash
from application.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_user, current_user
import pandas as pd
from fbprophet import Prophet

@app.route("/")
@app.route('/index')
def index():
    posts = Post.query.all()
    member = Member.query.all()
    return render_template('index.html', posts=posts, member=member, title="Welcome!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}; "Remember me" is {}'.format(form.username.data, form.remember_me.data), 'flash')
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'flash')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return "You have been registered"

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'flash')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/forecast')
def forecast():
   # Set a float format as we'll always be looking at USD monetary values
   pd.options.display.float_format = '${:,.2f}'.format
   # Read in hourly bitcoin price from conbase - price data provided via http://bitcoinity.org
   df = pd.read_csv(
       'http://data.bitcoinity.org/export_data.csv?currency=USD&data_type=price&exchange=coinbase&r=hour&t=l&timespan=30d',
       parse_dates=['Time'])

   # Set the date/time to be the index for the dataframe
   df.set_index('Time', inplace=True)
   df['ds'] = df.index
   df['y'] = df['avg']

   # read data
   forecast_data = df[['ds', 'y']].copy()
   forecast_data.reset_index(inplace=True)
   del forecast_data['Time']

   m = Prophet()
   m.fit(forecast_data);

   future = m.make_future_dataframe(periods=100, freq='H')

   forecasts = m.predict(future)
   forecasts = forecasts[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_json()

   return forecasts