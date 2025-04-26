# Health Information System API

A simple health information system API built with FastAPI that allows managing clients and health programs.

## Features

- Create and manage health programs (e.g., TB, Malaria, HIV)
- Register new clients
- Enroll clients in health programs
- Search for clients
- View client profiles and their enrolled programs
- **Authentication & Authorization**
  - Secure login system using OAuth2 with JWT tokens
  - Role-based access control (only doctors can create programs and enroll clients)
- **Data Validation**
  - Gender validation (must be "Male", "Female", or "Other")
  - Date of birth validation (must be in YYYY-MM-DD format)
- **Testing**
  - Comprehensive test suite using pytest
  - Tests for all major endpoints

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- `POST /token` - Login to get access token
  - Required fields: username, password
  - Default credentials: username="doctor", password="password123"

### Health Programs
- `POST /programs/` - Create a new health program (requires authentication)
- `GET /programs/` - List all health programs

### Clients
- `POST /clients/` - Register a new client (requires authentication)
- `GET /clients/` - List all clients
- `GET /clients/{client_id}` - Get a specific client's details
- `GET /clients/search/?query=search_term` - Search for clients

### Enrollments
- `POST /enrollments/` - Enroll a client in a health program (requires authentication)

## Data Validation

### Client Registration
- Gender must be one of: "Male", "Female", "Other"
- Date of birth must be in YYYY-MM-DD format
- All fields are required

## Testing

Run the test suite:
```bash
pytest
```

Tests cover:
- Program creation and listing
- Client registration and retrieval
- Client enrollment
- Search functionality
- Authentication and authorization

## Security

- Passwords are securely hashed using bcrypt
- JWT tokens expire after 30 minutes
- Protected endpoints require valid authentication
- Only users with "doctor" role can perform sensitive operations

## Example Usage

1. Login to get access token:
```json
POST /token
{
    "username": "doctor",
    "password": "password123"
}
```

2. Create a health program (include token in Authorization header):
```json
POST /programs/
{
    "name": "TB Program",
    "description": "Tuberculosis treatment and monitoring program"
}
```

3. Register a client:
```json
POST /clients/
{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "contact_number": "1234567890",
    "address": "123 Main St"
}
```

4. Enroll a client in a program:
```json
POST /enrollments/
{
    "client_id": 1,
    "program_id": 1
}
``` 