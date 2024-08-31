import os
import sys
import django

# Add the parent directory containing your Django project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AmpPay.settings')

# Initialize Django
django.setup()

# Now you can import Django models and perform your operations
from django.contrib.auth.models import User
from AmpPay.models import EnergyUsage
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Fetch data from Django database
data = EnergyUsage.objects.all().order_by('datetime').values('datetime', 'usage_value')

# Convert queryset to DataFrame
data_df = pd.DataFrame(data)

# Convert datetime to timezone-naive
data_df['datetime'] = pd.to_datetime(data_df['datetime']).dt.tz_localize(None)

# Set the datetime column as the index
data_df.set_index('datetime', inplace=True)

# Handle missing column or data
if 'usage_value' not in data_df.columns:
    raise ValueError("Column 'usage_value' not found in the DataFrame.")
elif data_df['usage_value'].isnull().any():
    raise ValueError("Missing values found in the 'usage_value' column.")

# Create features (X) and target (y)
X = data_df.index.to_julian_date().values.reshape(-1, 1)  # Convert datetime to Julian date
y = data_df['usage_value'].values

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate Mean Squared Error (MSE) to evaluate model performance
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse:.2f}")

# Predict energy usage at the end of the month
end_of_month_julian_date = pd.to_datetime('2024-08-31').to_julian_date()
predicted_usage = model.predict([[end_of_month_julian_date]])
print(f"Predicted usage at the end of the month: {predicted_usage[0]:.2f} units")
