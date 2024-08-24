from rest_framework import generics
from .models import EnergyUsage
from .serializers import EnergyUsageSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
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


class EnergyUsageList(generics.ListAPIView):
    serializer_class = EnergyUsageSerializer

    def get_queryset(self):
        return EnergyUsage.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['username_mapping'] = {user.id: user.username for user in User.objects.all()}
        return context
    
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        if not username:
            return JsonResponse({"error": "Username not provided"}, status=400)
        
        # Get the user object
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Create EnergyUsage instance
        energy_usage = EnergyUsage(
            user=user,
            # Assuming these fields are present in the data received from the Arduino
            irms_current=data.get('rms_current'),
            irms_power=data.get('rms_power'),
            usage_value=data.get('kilowatt_hours'),
            peak_power=data.get('peak_power')
        )
        energy_usage.save()

        return JsonResponse({"message": "Data received and stored successfully"}, status=200)
    else:
        return JsonResponse({"error": "Only POST requests are allowed"}, status=405)
    
@csrf_exempt
def predictenergyconsumption(req):
    #fetch data from db
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
    end_of_month_julian_date = pd.to_datetime('2024-03-29').to_julian_date()
    predicted_usage = model.predict([[end_of_month_julian_date]])
    print(f"Predicted usage at the end of the month: {predicted_usage[0]:.2f} units")
    response_data = {
        'predicted_usage': predicted_usage[0]
    }
    return JsonResponse(response_data)