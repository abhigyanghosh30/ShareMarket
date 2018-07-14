from flask import Flask, session, render_template, request, redirect, url_for, Response, json
from flask_sqlalchemy import SQLAlchemy
import os
import random


app = Flask(__name__)
app.secret_key = os.urandom(67)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'

db = SQLAlchemy(app)

# Models start here
#
#

class Investors(db.Model):
	__tablename__ = 'investors'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String)
	stocks1_count = db.Column(db.Integer, nullable=False, default=0)
	stocks2_count = db.Column(db.Integer, nullable=False, default=0)
	stocks3_count = db.Column(db.Integer, nullable=False, default=0)
	sales = db.relationship('Sales',backref='investors', lazy='dynamic')
	purchases = db.relationship('Purchases', primaryjoin="and_(Investors.id)==Purchases.recipient_id")

class Sales(db.Model):
	__tablename__ = 'sales'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('stocks.id'))
	amount = db.Column(db.Integer, nullable=False)

class Purchases(db.Model):
	__tablename__ = 'purchases'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	recipient_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('stocks.id'))
	amount = db.Column(db.Integer, nullable=False)

class Stocks(db.Model):
	__tablename__ = 'stocks'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	current_price = db.Column(db.Integer, nullable=False, default=100)
		
# Views start here
#
#

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/enter', methods=['POST'])
def enter():
	session.pop('name', None)
	name = request.form['name']
	password = request.form['password']
	session['name'] = name
	if name == 'admin' and password:
		return redirect(url_for('admin_home'))	
	return redirect('/home')

@app.route('/price', methods=['PUT'])
def price():
	data = request.get_json()
	print(data)
	stock = Stocks.query.filter_by(id=data['id']).first()
	print(stock)
	return Response(
		json.dumps({'price':stock.current_price}),
		status = 200,
		mimetype = 'application/json'
		)

@app.route('/home')
def home():
	return render_template('home.html', name=session['name'],stocks=Stocks.query.all())

@app.route('/admin_home')
def admin_home():
	investors=Investors.query.all()
	return render_template('admin_home.html', investors=investors)

@app.route('/sell')
def sell():
	investor = Investors.query.filter_by(name=session['name']).first()
	sale = Sales()
	return render_template('sell.html')

@app.route('/increase')
def increase():
	stock_id = request.form['']
	
	return redirect(url_for('home'))

@app.route('/buy')
def buy():
	return render_template('buy.html')

@app.route('/decrease')
def decrease():
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('name',None)
	return redirect('/login')


if __name__ == "__main__":
	app.run(debug=True)
