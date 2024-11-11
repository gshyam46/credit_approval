Credit Approval System
This project is a backend API for a Credit Approval System. The application enables customer and loan management with functionalities for checking credit eligibility, creating loans, and retrieving customer and loan details. The project is built using Django and Django REST Framework, with PostgreSQL as the database, and is fully containerized using Docker.

Project Structure
The main components of the project are:

Customers: Handles customer data including registration, and retrieving customer details.
Loans: Manages loan information including loan creation, eligibility checking, and loan detail retrieval.
Data Ingestion: Provides endpoints for importing customer and loan data from Excel files.
Features
Register a new customer.
Check loan eligibility based on customer’s credit score and income.
Create loans for eligible customers.
View all loans by customer.
View loan details by loan ID.
Ingest customer and loan data from Excel files.
Prerequisites
Ensure that you have the following installed:

Docker and Docker Compose
Python 3.9 or above (if running locally without Docker)
Pandas and Openpyxl packages for data ingestion from Excel files (these are included in requirements.txt)
Installation and Setup

1. Clone the Repository
   bash
   Copy code
   git clone (https://github.com/gshyam46/credit_approval.git)
   cd credit_approval
2. Environment Variables
   Create a .env file in the root directory to store environment variables for the database and Django settings. Example:

plaintext
Copy code
POSTGRES_DB=credit_approval
POSTGRES_USER=user
POSTGRES_PASSWORD=password
DJANGO_SECRET_KEY=your_secret_key_here 3. Docker Setup
Dockerfile
This project includes a Dockerfile for containerizing the Django app.

dockerfile
Copy code

# Dockerfile

FROM python:3.11.9-slim-bullseye

ENV PYTHONBUFFERED=1

ENV PORT 8080

# Set the working directory in the container

WORKDIR /app

# Copy the dependency file and install dependencies

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the project files into the container

COPY . /app/

# CMD gunicorn server.wsgi:application --bind 0.0.0.0:8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "credit_approval.wsgi:application"]

# Expose the port Django will run on

EXPOSE 8080

# Run the Django application

docker-compose up --build
-- then in another terminal
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
or

- not recommended
  (docker build -t credit_approval .
  docker run -p 8080:8080 credit_approval)

# you can test using postman

optional if you make changes
Step 1: Create Migrations
Run the following command to create migrations for your Django app:

docker-compose exec web python manage.py makemigrations
Step 2: Apply Migrations
Apply the migrations to create the necessary database tables:

docker-compose exec web python manage.py migrate
Step 3: Verify the Table Creation
After running the migrations, you can verify the table creation by connecting to the PostgreSQL container and running SQL commands:

Access the PostgreSQL container:

docker-compose exec db psql -U myuser -d mydatabase
Replace myuser with your PostgreSQL username and mydatabase with your database name.

List all tables:

sql
\dt
Check for the customers_customer table:

sql
SELECT \* FROM information_schema.tables WHERE table_name = 'customers_customer

docker build -t credit_approval .
docker run -p 8080:8080 credit_approval

To orchestrate the application and PostgreSQL services, use the docker-compose.yml file.

yaml
Copy code
version: '3'

services:
db:
image: postgres:13
environment:
POSTGRES_DB: ${POSTGRES_DB}
POSTGRES_USER: ${POSTGRES_USER}
POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
volumes: - postgres_data:/var/lib/postgresql/data

web:
build: .
command: python manage.py runserver 0.0.0.0:8080
volumes: - .:/app
ports: - "8080:8080"
depends_on: - db

volumes:
postgres_data: 4. Run Docker Containers
To build and start the Docker containers, use:

bash
Copy code
docker-compose up --build
This command will:

Build the Docker image
Start the PostgreSQL and Django containers
Expose the application on http://localhost:8080/
Running Migrations and Creating a Superuser
Once the containers are running, apply migrations and create a Django superuser.

docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
This sets up the database and enables access to the Django admin panel at http://localhost:8080/admin.

API Documentation
Below are the available endpoints for this application, including HTTP methods, parameters, and descriptions.

1. Customer Registration
   URL: /customers/register/
   Method: POST
   Description: Registers a new customer.
   Request Body:
   json
   Copy code
   {
   "first_name": "string",
   "last_name": "string",
   "age": "integer",
   "monthly_salary": "decimal",
   "phone_number": "string"
   }
   Response: Returns the registered customer details including approved_limit.
2. Check Loan Eligibility
   URL: /loans/check-eligibility/
   Method: POST
   Description: Checks if a customer is eligible for a loan.
   Request Body:
   json
   Copy code
   {
   "customer_id": "integer",
   "loan_amount": "decimal",
   "interest_rate": "decimal",
   "tenure": "integer"
   }
   Response: Provides approval status, interest rate, and monthly installment details.
3. Create Loan
   URL: /loans/create-loan/
   Method: POST
   Description: Creates a new loan for an eligible customer.
   Request Body:
   json
   Copy code
   {
   "customer_id": "integer",
   "loan_amount": "decimal",
   "interest_rate": "decimal",
   "tenure": "integer"
   }
   Response: Returns loan details including monthly installment.
4. View Loan Details
   URL: /loans/view-loan/<loan_id>/
   Method: GET
   Description: Retrieves loan details by loan_id.
   Response: Returns the loan and associated customer details.
5. View Loans by Customer
   URL: /loans/view-loans/<customer_id>/
   Method: GET
   Description: Retrieves all loans for a specific customer.
   Response: List of loans for the specified customer.
6. Ingest Customer Data
   URL: /customers/ingest/
   Method: GET
   Description: Reads data from customer_data.xlsx and imports it into the database.
   Response: Message indicating data ingestion status.
7. Ingest Loan Data
   URL: /loans/ingest/
   Method: GET
   Description: Reads data from loan_data.xlsx and imports it into the database.
   Response: Message indicating data ingestion status.
8. View All Loans
   URL: /loans/all-loans/
   Method: GET
   Description: Retrieves all loans in the database.
   Response: List of all loans.
   Data Ingestion Instructions
   Place customer_data.xlsx and loan_data.xlsx files in the directory specified in the ingestion views.
   Access the ingestion endpoints:
   For customer data: http://localhost:8080/customers/ingest/
   For loan data: http://localhost:8080/loans/ingest/
   These endpoints will import the data from the Excel files into the database.

Additional Information
Running the Application without Docker
If you prefer to run the project locally:

Set up a virtual environment and activate it.
bash
Copy code
python -m venv env
source env/bin/activate # On Windows use `env\Scripts\activate`
Install dependencies.
bash
Copy code
pip install -r requirements.txt
Apply migrations and start the server.
bash
Copy code
python manage.py migrate
python manage.py runserver
Accessing the Django Admin
Visit http://localhost:8080/admin and log in with the superuser credentials you created. This admin interface allows you to manage customer and loan data manually.

Notes
Ensure that customer_data.xlsx and loan_data.xlsx files are up-to-date and correctly formatted before ingestion.
Duplicate records are handled by using get_or_create in the ingestion views.
For Docker, the db service name must match the HOST value in settings.py.
