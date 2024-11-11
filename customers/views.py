
from .serializers import CustomerSerializer
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer


class IngestCustomerDataView(APIView):
    def get(self, request):
        try:
            # Load data from Excel file
            df = pd.read_excel('./data/customer_data.xlsx')

            # Iterate over DataFrame rows and add customers to the database
            for _, row in df.iterrows():
                Customer.objects.get_or_create(
                    customer_id=row['customer_id'],
                    defaults={
                        "first_name": row['first_name'],
                        "last_name": row['last_name'],
                        "phone_number": row['phone_number'],
                        "monthly_salary": row['monthly_salary'],
                        "approved_limit": row['approved_limit'],
                        "current_debt": row['current_debt'],
                    }
                )

            return Response({"message": "Customer data ingested successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterCustomer(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            monthly_salary = serializer.validated_data.get('monthly_salary')
            serializer.save(approved_limit=round(36 * monthly_salary, -5))
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CustomerListView(APIView):
    def get(self, request):
        customers = Customer.objects.all()  # Retrieve all customers
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)
