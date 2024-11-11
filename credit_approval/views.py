from django.http import JsonResponse


def api_overview(request):
    instructions = {
        "message": "Welcome to the Credit Approval System API",
        "instructions": "Below are the available API endpoints with their descriptions.",
        "endpoints": {
            "/customers/register/": "POST - Register a new customer.",
            "/customers/list/": "GET - Retrieve a list of all customers.",
            "/customers/ingest/": "GET - Ingest customer data from customer_data.xlsx file.",

            "/loans/check-eligibility/": "POST - Check loan eligibility for a customer.",
            "/loans/create-loan/": "POST - Create a new loan for a customer.",
            "/loans/view-loan/<loan_id>/": "GET - View loan details by loan ID.",
            "/loans/view-loans/<customer_id>/": "GET - View all loans for a specific customer.",
            "/loans/all-loans/": "GET - Retrieve a list of all loans in the system.",
            "/loans/ingest/": "GET - Ingest loan data from loan_data.xlsx file."
        }

    }
    return JsonResponse(instructions)
