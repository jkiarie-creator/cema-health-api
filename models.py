from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class HealthProgram(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime = datetime.now()

class Client(BaseModel):
    id: int
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    contact_number: str
    address: str
    enrolled_programs: List[int] = []  # List of program IDs
    created_at: datetime = datetime.now()

class ClientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    contact_number: str
    address: str

class ProgramCreate(BaseModel):
    name: str
    description: str

class ProgramEnrollment(BaseModel):
    client_id: int
    program_id: int 