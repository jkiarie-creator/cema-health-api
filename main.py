from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from typing import List
from models import Client, HealthProgram, ClientCreate, ProgramCreate, ProgramEnrollment
from datetime import datetime
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, status
from datetime import timedelta

app = FastAPI(title="Health Information System API")

# In-memory storage (in a real application, this would be a database)
clients = {}
health_programs = {}
next_client_id = 1
next_program_id = 1

# Secret key for JWT
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dummy user database (replace with real DB in production)
fake_users_db = {
    "doctor": {
        "username": "doctor",
        "full_name": "Dr. John Doe",
        "hashed_password": pwd_context.hash("password123"),
        "role": "doctor",
    }
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = fake_users_db.get(username)
    if user is None:
        raise credentials_exception
    return user

def doctor_required(user: dict = Depends(get_current_user)):
    if user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@app.post("/programs/", response_model=HealthProgram)
async def create_program(program: ProgramCreate, user: dict = Depends(doctor_required)):
    global next_program_id
    program_id = next_program_id
    new_program = HealthProgram(
        id=program_id,
        name=program.name,
        description=program.description
    )
    health_programs[program_id] = new_program
    next_program_id += 1
    return new_program

@app.get("/programs/", response_model=List[HealthProgram])
async def list_programs():
    return list(health_programs.values())

@app.post("/clients/", response_model=Client)
async def create_client(client: ClientCreate, user: dict = Depends(doctor_required)):
    global next_client_id
    client_id = next_client_id
    new_client = Client(
        id=client_id,
        first_name=client.first_name,
        last_name=client.last_name,
        date_of_birth=client.date_of_birth,
        gender=client.gender,
        contact_number=client.contact_number,
        address=client.address
    )
    clients[client_id] = new_client
    next_client_id += 1
    return new_client

@app.get("/clients/", response_model=List[Client])
async def list_clients():
    return list(clients.values())

@app.get("/clients/{client_id}", response_model=Client)
async def get_client(client_id: int):
    if client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    return clients[client_id]

@app.post("/enrollments/")
async def enroll_client(enrollment: ProgramEnrollment, user: dict = Depends(doctor_required)):
    if enrollment.client_id not in clients:
        raise HTTPException(status_code=404, detail="Client not found")
    if enrollment.program_id not in health_programs:
        raise HTTPException(status_code=404, detail="Program not found")
    
    client = clients[enrollment.client_id]
    if enrollment.program_id not in client.enrolled_programs:
        client.enrolled_programs.append(enrollment.program_id)
    return {"message": "Client enrolled successfully"}

@app.get("/clients/search/")
async def search_clients(query: str):
    results = []
    for client in clients.values():
        if (query.lower() in client.first_name.lower() or 
            query.lower() in client.last_name.lower() or 
            query.lower() in client.contact_number):
            results.append(client)
    return results

# Login endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Custom landing page
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Health Information System</title>
            <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Poppins', sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 {
                    color: #2c3e50;
                }
                .links {
                    margin-top: 20px;
                }
                a {
                    display: inline-block;
                    margin-right: 20px;
                    color: #3498db;
                    text-decoration: none;
                }
                a:hover {
                    text-decoration: underline;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Health Information System API</h1>
            <p>This API allows you to manage health programs and client information.</p>
            
            <div class="links">
                <h2>API Documentation:</h2>
                <a href="/docs">Swagger UI</a>
                <a href="/redoc">ReDoc</a>
            </div>
            
            <div class="links">
                <h2>Available Endpoints:</h2>
                <ul>
                    <li><strong>Authentication:</strong> POST /token</li>
                    <li><strong>Programs:</strong> GET /programs/, POST /programs/</li>
                    <li><strong>Clients:</strong> GET /clients/, POST /clients/, GET /clients/{id}</li>
                    <li><strong>Enrollments:</strong> POST /enrollments/</li>
                </ul>
            </div>
        </body>
    </html>
    """ 