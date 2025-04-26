# Health Information System API

A simple health information system API built with FastAPI that allows managing clients and health programs.

## Features

- Create and manage health programs (e.g., TB, Malaria, HIV)
- Register new clients
- Enroll clients in health programs
- Search for clients
- View client profiles and their enrolled programs

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

### Health Programs
- `POST /programs/` - Create a new health program
- `GET /programs/` - List all health programs

### Clients
- `POST /clients/` - Register a new client
- `GET /clients/` - List all clients
- `GET /clients/{client_id}` - Get a specific client's details
- `GET /clients/search/?query=search_term` - Search for clients

### Enrollments
- `POST /enrollments/` - Enroll a client in a health program

## Example Usage

1. Create a health program:
POST /programs/
```json
{
    "name": "TB Program",
    "description": "Tuberculosis treatment and monitoring program"
}
```

2. Register a client:
POST /clients/
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "date_of_birth": "1990-01-01",
    "gender": "Male",
    "contact_number": "1234567890",
    "address": "123 Main St"
}
```

3. Enroll a client in a program:
POST /enrollments/
```json
{
    "client_id": 1,
    "program_id": 1
}
``` 