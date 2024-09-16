"""
URL configuration for AmpPay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import EnergyUsageList
from .views import receive_data
from .views import predictenergyconsumption
# from .views import send_data_to_arduino




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/energyusage/', EnergyUsageList.as_view(), name='energyusage-list-create'),
    path('api/receive-data/', receive_data, name='receive_data'),
    path('api/predictenergyconsumption',predictenergyconsumption, name='predictenergyconsumption'),
    # path('send_data_to_arduino/', send_data_to_arduino, name='send_data_to_arduino'),
]
