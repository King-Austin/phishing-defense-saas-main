import joblib
from sklearn.metrics import confusion_matrix, classification_report

# Load the trained model
model = joblib.load('models/phishing_model.pkl')

# Load the saved X_test and y_test
X_test = joblib.load('models/X_test.pkl')
y_test = joblib.load('models/y_test.pkl')

# Predict using the model
y_pred = model.predict(X_test)

# Evaluate the performance
# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print("Confusion Matrix:")
print(cm)

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Calculate accuracy
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy}")
