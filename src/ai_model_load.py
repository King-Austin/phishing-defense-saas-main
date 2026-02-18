import pandas as pd

# Load the dataset
data = pd.read_csv('datasets/Nigerian_Fraud.csv')  # Adjust the path as needed

# Display the first few rows to inspect the data
print(data.head())

# Display column names to understand the structure
print(data.columns)
