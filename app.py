from flask import Flask, render_template, request, redirect, url_for, flash, session
import joblib
import os
import pandas as pd 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

# Load model and vectorizer
model_path = os.path.join('models', 'phishing_model.pkl')
vectorizer_path = os.path.join('models', 'vectorizer.pkl')
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get input email text
        email_text = request.form['email_text']

         # Check for minimum input length
        if len(email_text.split()) < 10:
            flash("Please provide a more detailed email for accurate detection.", 'error')
            return render_template('index.html')

        # Preprocess and predict
        email_vector = vectorizer.transform([email_text])
        prediction = model.predict(email_vector)[0]

        # Display result
        result = 'Phishing' if prediction == 1 else 'Not Phishing'
        return render_template('index.html', prediction=result, email_text=email_text)

    return render_template('index.html', prediction=None)

feedback_file = 'feedback_data.csv'
@app.route('/feedback', methods=['POST'])
def feedback():
    email_text = request.form['email_text']
    prediction = request.form['prediction']
    feedback = request.form['feedback']
    
    # Save to feedback file
    df = pd.DataFrame([[email_text, prediction, feedback]], columns=['email_text', 'prediction', 'feedback'])
    if os.path.exists(feedback_file):
        df.to_csv(feedback_file, mode='a', header=False, index=False)
    else:
        df.to_csv(feedback_file, index=False)
    
    # Use flash instead of passing message in the URL
    flash("Feedback received. Thank you!", 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
