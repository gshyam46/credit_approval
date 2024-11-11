
from .serializers import LoanSerializer
import math
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Loan
from customers.models import Customer


class IngestLoanDataView(APIView):
    def get(self, request):
        try:
            # Load data from Excel file
            df = pd.read_excel('/app/loans/loanData/loan_data.xlsx')

            # Iterate over DataFrame rows and add loans to the database
            for _, row in df.iterrows():
                if pd.isnull(row[['Customer ID', 'Loan ID', 'Loan Amount', 'Tenure', 'Interest Rate', 'Monthly payment', 'EMIs paid on Time', 'Date of Approval', 'End Date']]).any():
                    continue  # Skip rows with any null values
                customer = Customer.objects.get(customer_id=row['Customer ID'])
                Loan.objects.get_or_create(
                    loan_id=row['Loan ID'],
                    defaults={
                        "customer": customer,
                        "loan_amount": row['Loan Amount'],
                        "tenure": row['Tenure'],
                        "interest_rate": row['Interest Rate'],
                        "monthly_repayment": row['Monthly payment'],
                        "emis_paid_on_time": row['EMIs paid on Time'],
                        "start_date": row['Date of Approval'],
                        "end_date": row['End Date'],
                    }
                )

            return Response({"message": "Loan data ingested successfully"}, status=status.HTTP_201_CREATED)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found for one or more loans"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckEligibilityView(APIView):
    def post(self, request):
        customer_id = request.data.get('customer_id')
        loan_amount = request.data.get('loan_amount')
        interest_rate = request.data.get('interest_rate')
        tenure = request.data.get('tenure')

        try:
            customer = Customer.objects.get(customer_id=customer_id)

            # Example eligibility logic:
            # Assuming the customer’s approved credit limit is required for basic eligibility.
            # Modify this as per the specific eligibility rules.
            if customer.current_debt + loan_amount > customer.approved_limit:
                return Response({
                    "customer_id": customer_id,
                    "approval": False,
                    "message": "Loan amount exceeds approved credit limit",
                }, status=status.HTTP_400_BAD_REQUEST)

            # If eligible, calculate monthly installment
            monthly_installment = (loan_amount * (interest_rate / 100) * math.pow(
                (1 + interest_rate / 100), tenure)) / (math.pow((1 + interest_rate / 100), tenure) - 1)

            # Response with eligibility and calculated values
            return Response({
                "customer_id": customer_id,
                "approval": True,
                "interest_rate": interest_rate,
                # Set corrected interest rate if any adjustments needed
                "corrected_interest_rate": interest_rate,
                "tenure": tenure,
                "monthly_installment": round(monthly_installment, 2)
            }, status=status.HTTP_200_OK)

        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)


class AllLoansView(APIView):
    def get(self, request):
        loans = Loan.objects.all()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


class CreateLoanView(APIView):
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoanDetailView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        except Loan.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CustomerLoansView(APIView):
    def get(self, request, customer_id):
        loans = Loan.objects.filter(customer_id=customer_id)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
