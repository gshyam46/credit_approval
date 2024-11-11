from django.urls import path
from .views import CreateLoanView, IngestLoanDataView, LoanDetailView, CustomerLoansView, CheckEligibilityView, AllLoansView

urlpatterns = [
    path('create-loan/', CreateLoanView.as_view(), name='create-loan'),
    path('view-loan/<int:loan_id>/', LoanDetailView.as_view(), name='view-loan'),
    path('view-loans/<int:customer_id>/',
         CustomerLoansView.as_view(), name='view-customer-loans'),
    path('check-eligibility/', CheckEligibilityView.as_view(),
         name='check-eligibility'),
    path('all-loans/', AllLoansView.as_view(), name='all-loans'),
    path('ingest/', IngestLoanDataView.as_view(), name='ingest-loan-data'),
]
