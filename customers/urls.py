from django.urls import path
from .views import IngestCustomerDataView, RegisterCustomer, CustomerListView

urlpatterns = [
    path('register/', RegisterCustomer.as_view(), name='register-customer'),
    path('list/', CustomerListView.as_view(), name='list-customers'),
    path('ingest/', IngestCustomerDataView.as_view(),
         name='ingest-customer-data'),
]
