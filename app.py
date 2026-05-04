from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import os
import pandas as pd

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# ===== Flask-Login Setup =====
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access PhishGuard AI.'
login_manager.login_message_category = 'info'

# ===== In-Memory User Store =====
users = {}

class User(UserMixin):
    def __init__(self, id, username, password_hash):
        self.id = id
        self.username = username
        self.password_hash = password_hash

# Create default admin user
default_user = User(
    id='1',
    username='admin',
    password_hash=generate_password_hash('Myproject2026')
)
users['admin'] = default_user

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

# ===== Auth Routes =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        user = users.get(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Welcome back! You are now logged in.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
        elif len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
        elif password != confirm_password:
            flash('Passwords do not match.', 'error')
        elif username in users:
            flash('Username already exists. Please choose another.', 'error')
        else:
            new_id = str(len(users) + 1)
            new_user = User(
                id=new_id,
                username=username,
                password_hash=generate_password_hash(password)
            )
            users[username] = new_user
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# ===== Load model and vectorizer =====
model_path = os.path.join('models', 'phishing_model.pkl')
vectorizer_path = os.path.join('models', 'vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

# ===== Main App Routes =====
@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        email_text = request.form['email_text']

        if len(email_text.split()) < 10:
            flash("Please provide a more detailed email for accurate detection.", 'error')
            return render_template('index.html')

        email_vector = vectorizer.transform([email_text])
        prediction = model.predict(email_vector)[0]
        
        # Calculate confidence score
        probabilities = model.predict_proba(email_vector)[0]
        confidence = round(max(probabilities) * 100, 2)

        result = 'Phishing' if prediction == 1 else 'Not Phishing'
        return render_template('index.html', prediction=result, confidence=confidence, email_text=email_text)

    return render_template('index.html', prediction=None)

feedback_file = 'feedback_data.csv'

@app.route('/feedback', methods=['POST'])
@login_required
def feedback():
    email_text = request.form['email_text']
    prediction = request.form['prediction']
    feedback = request.form['feedback']

    df = pd.DataFrame([[email_text, prediction, feedback]], columns=['email_text', 'prediction', 'feedback'])
    if os.path.exists(feedback_file):
        df.to_csv(feedback_file, mode='a', header=False, index=False)
    else:
        df.to_csv(feedback_file, index=False)

    flash("Feedback received. Thank you!", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
