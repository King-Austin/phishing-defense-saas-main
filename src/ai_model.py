import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle
import joblib

# Load dataset
data = pd.read_csv('datasets/CEAS_08.csv')

# Convert columns to strings to avoid concatenation errors
data['subject'] = data['subject'].astype(str)
data['body'] = data['body'].astype(str)
data['urls'] = data['urls'].astype(str)

# Combine 'subject', 'body', and 'urls' into one column for training
data['combined_text'] = data['subject'] + " " + data['body'] + " " + data['urls']

# Preprocess data
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X = vectorizer.fit_transform(data['combined_text']) #Using the combined column
y = data['label']

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save X_test and y_test for evaluation
joblib.dump(X_test, 'models/X_test.pkl')
joblib.dump(y_test, 'models/y_test.pkl')

# Save the trained model and vectorizer for future use
joblib.dump(model, 'models/phishing_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')  # Save the vectorizer

# Test accuracy
y_pred = model.predict(X_test)
print(f"Model Accuracy: {accuracy_score(y_test, y_pred)}")

