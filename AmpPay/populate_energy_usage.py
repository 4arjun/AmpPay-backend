import os
import sys
import django
import time

# Add the parent directory containing your Django project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AmpPay.settings')

# Initialize Django
django.setup()

# Now you can import Django models and perform your operations
from django.contrib.auth.models import User



from django.contrib.auth.models import User
from AmpPay.models import EnergyUsage
from datetime import datetime, timedelta
import random

user = User.objects.get(username='Arjun')

# Define parameters for data generation
start_year = 2024
start_month = 8  # January
num_months = 1  # Generate data for 3 months
days_in_month = [30]  # Days in January, February, March

initial_usage_value = 1.0
daily_usage_increment = 1.0  # Increment in usage value per day

# Loop through each month
for i in range(num_months):
    year = start_year
    month = start_month + i
    num_days = days_in_month[i]

    current_usage_value = initial_usage_value

    # Generate data for each day in the month
    for day in range(1, num_days + 1):
        for hour in range(24):
            # Generate random values for each field
            datetime_value = datetime(year, month, day, hour)
            usage_value = current_usage_value  # Set current usage value

            irms_current = random.uniform(0, 10)  # Example range for irms_current
            irms_power = random.uniform(0, 20)  # Example range for irms_power
            peak_power = random.uniform(0, 30)  # Example range for peak_power

            # Create an instance of EnergyUsage
            energy_usage = EnergyUsage.objects.create(
                user=user,
                datetime=datetime_value,
                usage_value=usage_value,
                irms_current=irms_current,
                irms_power=irms_power,
                peak_power=peak_power
            )

            # Save the instance to the database
            energy_usage.save()
            time.sleep(0.01)
            

        # Increment the current usage value for the next day
        current_usage_value += daily_usage_increment

    # Reset current usage value for the next month
    initial_usage_value = current_usage_value

print("Data generation completed.")