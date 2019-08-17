from flask import Flask,render_template,request,session,redirect,url_for
from model import check_user,add_user_to_db,check_product,add_product_to_db,get_products,remove_product

app = Flask(__name__)
app.secret_key = 'hello'

@app.route('/')
def home():
	return  render_template('home.html',title='home')

@app.route('/about')
def about():
	return render_template('about.html',title='about')

@app.route('/contact')
def contact():
	return render_template('contact.html',title='contact')

@app.route('/signup',methods=['GET','POST'])
def signup():

	if request.method == 'POST':

		user_info = {}

		user_info['username'] = request.form['username']
		user_info['full_name'] = request.form['full_name']
		user_info['password'] = request.form['password1']
		rpassword = request.form['password2']
		user_info['email'] = request.form['email']
		user_info['c_type'] = request.form['c_type']

		if user_info['password']!=rpassword:
			return "Passwords don't match.Go back and re-enter"

		if bool(check_user(user_info['username'])) is True:
			return "User already exists. Try logging in!"

		if user_info['c_type'] == 'buyer':
			user_info['cart'] = []

		add_user_to_db(user_info)
		session['username'] = user_info['username'] 
		session['c_type'] = user_info['c_type']
		return redirect(url_for('home'))

	return redirect(url_for('home'))

@app.route('/login',methods=['GET','POST'])
def login():

	if request.method == 'POST':
	
		username = request.form['username']
		password = request.form['password']

		if bool(check_user(username)) and (check_user(username)['password'] == password): 
			session['username'] = username
			session['c_type'] = check_user(username)['c_type']
			return redirect(url_for('home'))
		return "Username or password incorrect.Try again"
	return redirect(url_for('home'))

@app.route('/products',methods=['GET','POST'])
def products():

	if request.method == 'POST':
		product_info = {}
		product_info['name'] = request.form['name']
		product_info['info'] = request.form['info']
		product_info['price'] = int(request.form['price'])
		product_info['seller'] = session['username']

		if bool(check_product(product_info['name'])) is True:
			return "Product already exists!"

		add_product_to_db(product_info)
		return redirect(url_for('home'))

	products = get_products()
	return render_template('products.html',products=products)

@app.route('/remove',methods=['GET','POST'])
def remove():

	if request.method == 'POST':
		name = request.form['name']
		remove_product(name)
		return redirect(url_for('products'))

	return redirect(url_for('products'))

@app.route('/logout')
def logout():

	session.clear()
	return redirect(url_for('home'))

app.run(debug=True)