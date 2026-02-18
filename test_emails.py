import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Load the trained model
model = joblib.load('phishing_model.pkl')

# Load your test emails (ensure the CSV has the same format as the training data)
# Replace 'your_emails.csv' with the actual path to your email file
test_data = pd.read_csv('test_email.csv')

# Combine the 'subject', 'body', and 'urls' columns to create a unified text field
test_data['combined_text'] = test_data['subject'].astype(str) + " " + test_data['body'].astype(str) + " " + test_data['urls'].astype(str)

# Load the TfidfVectorizer used during training
vectorizer = joblib.load('vectorizer.pkl')

# Transform the test emails using the vectorizer
X_test = vectorizer.transform(test_data['combined_text'])

# Make predictions
predictions = model.predict(X_test)

# Print out the results
test_data['predictions'] = predictions
test_data['predictions'] = test_data['predictions'].map({0: 'Legitimate', 1: 'Phishing'})

# Display the results
print(test_data[['subject', 'body', 'urls', 'predictions']])

# Optionally, save the results to a CSV file
test_data.to_csv('email_classification_results.csv', index=False)
