from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  
app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'myapp'

mysql = MySQL(app)

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()

        flash('Signup successful. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Login route
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()  # Fetch one row

        if user is not None and user[2] == password:
            session['logged_in'] = True
            session['username'] = username
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Please try again.', 'danger')
        
        cursor.close()

    return render_template('login.html')


# Dashboard route (a protected route)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f'Welcome, {session["username"]}! This is your dashboard.'
    else:
        flash('Please log in first.', 'danger')
        return redirect(url_for('login'))

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

