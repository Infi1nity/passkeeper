from fastapi import FastAPI, Depends, HTTPException
from typing import List
from database import get_db, engine, Base, SessionLocal
from schemas import ServiceResponse, ServiceCreate, ServiceWithPasswords
from sqlalchemy.orm import Session
from models import Service

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
