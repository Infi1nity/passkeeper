from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import get_db, engine, Base, SessionLocal
from schemas import ServiceResponse, ServiceCreate, ServiceWithPasswords, PasswordCreate, PasswordResponse
from sqlalchemy.orm import Session
from models import Service, Password

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post('/services/', response_model=ServiceResponse)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    new_service = Service(
        name = service.name,
        description = service.description,
    )

    db.add(new_service)
    db.commit()
    db.refresh(new_service)
    return new_service

@app.get('/services', response_model=List[ServiceResponse])
def get_services(db: Session = Depends(get_db)):
    query = db.query(Service)
    services = query.all()
    return services

@app.get('/services/{id}', response_model=ServiceWithPasswords)
def get_service(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if not service:
        raise HTTPException(404, detail='Service not found')

    return service

@app.delete('/services/{id}', response_model=ServiceResponse)
def delete_service(id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == id).first()
    if not service:
        raise HTTPException(404, detail='Service not found')

    db.delete(service)
    db.commit()
    
    return service

@app.post('/passwords', response_model=PasswordResponse)
def create_password(password_data: PasswordCreate, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == password_data.service_id).first()
    if not service:
        raise HTTPException(404, detail='Service not found')

    new_password = Password(
        username = password_data.username,
        password = password_data.password,
        service_id = password_data.service_id,
        notes=password_data.notes
    )

    db.add(new_password)
    db.commit()
    db.refresh(new_password)
    
    return new_password

@app.get('/passwords', response_model=list[PasswordResponse])
def list_passwords(db: Session = Depends(get_db)):
    passwords = db.query(Password).all()
    
    return passwords

@app.get('/passwords/{id}', response_model=PasswordResponse)
def list_password(id: int, db: Session = Depends(get_db)):
    password = db.query(Password).filter(Password.id == id).first()
    if not password:
        raise HTTPException(status_code=404, detail=f"Password with ID: {id} not found")
    
    return password

@app.delete('/passwords/{id}', response_model=PasswordResponse)
def delete_password(id: int, db: Session = Depends(get_db)):
    password = db.query(Password).filter(Password.id == id).first()
    if not password:
        raise HTTPException(status_code=404, detail=f"Password with ID: {id} not found")

    db.delete(password)
    db.commit()

    return password