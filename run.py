from flask import Flask, session, render_template, request, redirect, url_for, Response, json
from flask_sqlalchemy import SQLAlchemy
import os
import random
import subprocess

app = Flask(__name__)
app.secret_key = os.urandom(67)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'

result = []
win_cmd = 'ipconfig'
process = subprocess.check_output(win_cmd).decode()
print(process)
print(process.index('192'))
index = process.index('192')
IP = ""
for i in range(13):
    IP = IP+process[index+i]
print(IP)
db = SQLAlchemy(app)

# Models start here
#
#

class Investors(db.Model):
	__tablename__ = 'investors'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String)
	stocks1 = db.Column(db.Integer, nullable=False, default=0)
	stocks2 = db.Column(db.Integer, nullable=False, default=0)
	stocks3 = db.Column(db.Integer, nullable=False, default=0)
	stocks4 = db.Column(db.Integer, nullable=False, default=0)
	stocks5 = db.Column(db.Integer, nullable=False, default=0)
	stocks6 = db.Column(db.Integer, nullable=False, default=0)
	stocks7 = db.Column(db.Integer, nullable=False, default=0)
	stocks8 = db.Column(db.Integer, nullable=False, default=0)
	stocks9 = db.Column(db.Integer, nullable=False, default=0)
	stocks10 = db.Column(db.Integer, nullable=False, default=0)
	stocks11 = db.Column(db.Integer, nullable=False, default=0)
	stocks12 = db.Column(db.Integer, nullable=False, default=0)
	stocks13 = db.Column(db.Integer, nullable=False, default=0)
	stocks14 = db.Column(db.Integer, nullable=False, default=0)
	stocks15 = db.Column(db.Integer, nullable=False, default=0)
	sales = db.relationship('Sales',backref='investors', lazy='dynamic')
	purchases = db.relationship('Purchases', primaryjoin="and_(Investors.id)==Purchases.recipient_id")
	amount_left = db.Column(db.Integer, nullable=False, default=0)

class Sales(db.Model):
	__tablename__ = 'sales'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	sender_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
	amount = db.Column(db.Integer, nullable=False)

class Purchases(db.Model):
	__tablename__ = 'purchases'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	recipient_id = db.Column(db.Integer, db.ForeignKey('investors.id'))
	stock_id = db.Column(db.Integer,db.ForeignKey('companies.id'))
	amount = db.Column(db.Integer, nullable=False)

class Companies(db.Model):
	__tablename__ = 'companies'
	
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100), nullable=False)
	current_price = db.Column(db.Integer, nullable=False, default=100)
	shares_left = db.Column(db.Integer, nullable=False, default=100)	


### CHECK SELL AND BUY CONDITIONS
###
###
def checksell(stockid,nos,investor):
	# investor = Investors.query.filter_by(name=session['name']).first()
	if( stockid == 1 and investor.stocks1 > nos ):
			return True
	if( stockid == 2 and investor.stocks2 > nos ):
			return True
	if( stockid == 3 and investor.stocks3 > nos ):
			return True
	if( stockid == 4 and investor.stocks4 > nos ):
			return True
	if( stockid == 5 and investor.stocks5 > nos ):
			return True
	if( stockid == 6 and investor.stocks6 > nos ):
			return True
	if( stockid == 7 and investor.stocks7 > nos ):
			return True
	if( stockid == 8 and investor.stocks8 > nos ):
			return True
	if( stockid == 9 and investor.stocks9 > nos ):
			return True
	if( stockid == 10 and investor.stocks10 > nos ):
			return True
	if( stockid == 11 and investor.stocks11 > nos ):
			return True
	if( stockid == 12 and investor.stocks12 > nos ):
			return True
	if( stockid == 13 and investor.stocks13 > nos ):
			return True
	if( stockid == 14 and investor.stocks14 > nos ):
			return True
	if( stockid == 15 and investor.stocks15 > nos ):
			return True
	return False

def checkbuy(stockid,nos,investor,stock):
	# investor = Investors.query.filter_by(name = session['name']).first()
	# stock = Stock.query.filter_by(id = stockid).first()
	nos=int(nos)
	print(type(stock.current_price))
	print(type(nos))
	print(nos)

	if investor.amount_left > stock.current_price * nos and stock.shares_left > nos :
		if stockid == 1 :
			investor.stocks1 += nos
		if stockid == 2 :
			investor.stocks2 += nos
		if stockid == 3 :
			investor.stocks3 += nos
		if stockid == 4 :
			investor.stocks4 += nos
		if stockid == 5 :
			investor.stocks5 += nos
		if stockid == 6 :
			investor.stocks6 += nos
		if stockid == 7 :
			investor.stocks7 += nos
		if stockid == 8 :
			investor.stocks8 += nos
		if stockid == 9 :
			investor.stocks9 += nos
		if stockid == 10 :
			investor.stocks10 += nos
		if stockid == 11 :
			investor.stocks11 += nos
		if stockid == 12 :
			investor.stocks12 += nos
		if stockid == 13 :
			investor.stocks13 += nos
		if stockid == 14 :
			investor.stocks14 += nos
		if stockid == 15 :
			investor.stocks15 += nos
		
		db.session.commit()
		return True
	return False

#### Views start here
###
###

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/enter', methods=['POST'])
def enter():
	session.pop('name', None)
	name = request.form['name']
	password = request.form['password']
	try:
		if name == 'admin' and password == 'admin123' :
			session['name'] = name
			return redirect(url_for('admin_home'))
		investor = Investors.query.filter_by(username=name).first()
		if(password == investor.password):
			session['name'] = name
			return redirect('/home')
		session['name'] = name
		return redirect('/home')
	except:
		return redirect('/')

@app.route('/price', methods=['PUT'])
def price():
	data = request.get_json()
	stock = Companies.query.filter_by(id=data['id']).first()
	return Response(
		json.dumps({'price':stock.current_price}),
		status = 200,
		mimetype = 'application/json'
		)

@app.route('/home')
def home():
	return render_template('home.html', name=session['name'],stocks=Companies.query.all())

@app.route('/admin_home')
def admin_home():
	investors=Investors.query.all()
	return render_template('admin_home.html', investors=investors)

@app.route('/sell')
def sell():
	return render_template('sell.html')

@app.route('/decrease',methods=['POST'])
def decrease():
	number_of_stocks = request.form['number']
	stock_id = request.form['stock_id']
	
	investor = Investors.query.filter_by(name=session['name']).first()
	stock = Companies.query.filter_by(id=stock_id).first()

	if checksell(stock_id,number_of_stocks,investor):
		investor.amount_left += stock.current_price * number_of_stocks
		sale = Sales(sender_id=investor.id,stock_id=stock_id,amount=stock.current_price,number_of_stocks=number_of_stocks)
		stock.amount_left += number_of_stocks
		stock.current_price -= 1 	
		db.session.add(sale)
		db.session.commit()

	return redirect(url_for('home'))

@app.route('/buy')
def buy():
	return render_template('buy.html')

@app.route('/increase',methods=['POST'])
def increase():
	number_of_stocks = request.form['number']
	stock_id = request.form['stock_id']
	
	investor = Investors.query.filter_by(name=session['name']).first()
	stock = Companies.query.filter_by(id=stock_id).first()

	if checkbuy(stock_id,number_of_stocks,investor,stock):
		investor.amount_left -= stock.current_price * number_of_stocks
		purchase = Purchases(recipient_id=investor.id,stock_id=stock_id,amount=stock.current_price,number_of_stocks=number_of_stocks)
		stock.amount_left -= number_of_stocks
		stock.current_price += 2
		db.session.add(purchase)
		db.session.commit()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('name',None)
	return redirect('/login')

@app.route('/admin_change')
def admin_change():
	pass

@app.route('/change')
def change():
	pass

if __name__ == "__main__":
	app.run(host=IP,port=5000,debug=True)
