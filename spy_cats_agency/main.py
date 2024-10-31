# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base
from schemas import SpyCatCreate, SpyCat, MissionCreate, Mission, Target
import crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/spycats/", response_model=SpyCatCreate)
def create_spycat(spycat: SpyCatCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_spycat(db=db, spycat=spycat)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/spycats/{spycat_id}", response_model=SpyCat)
def read_spycat(spycat_id: int, db: Session = Depends(get_db)):
    db_spycat = crud.get_spycat(db, spycat_id=spycat_id)
    if db_spycat is None:
        raise HTTPException(status_code=404, detail="SpyCat not found")
    return db_spycat

@app.get("/spycats/", response_model=list[SpyCat])
def read_spycats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_spycats(db, skip=skip, limit=limit)

@app.put("/spycats/{spycat_id}", response_model=SpyCat)
def update_spycat_salary(spycat_id: int, new_salary: float, db: Session = Depends(get_db)):
    db_spycat = crud.update_spycat_salary(db, spycat_id=spycat_id, new_salary=new_salary)
    if db_spycat is None:
        raise HTTPException(status_code=404, detail="SpyCat not found")
    return db_spycat

@app.delete("/spycats/{spycat_id}", response_model=SpyCat)
def delete_spycat(spycat_id: int, db: Session = Depends(get_db)):
    db_spycat = crud.delete_spycat(db, spycat_id=spycat_id)
    if db_spycat is None:
        raise HTTPException(status_code=404, detail="SpyCat not found")
    return db_spycat

@app.post("/missions/", response_model=Mission)
def create_mission(mission: MissionCreate, cat_id: int, db: Session = Depends(get_db)):
    return crud.create_mission(db=db, mission_data=mission, cat_id=cat_id)

@app.get("/missions/{mission_id}", response_model=Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = crud.get_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found")
    return db_mission

@app.get("/missions/", response_model=list[Mission])
def read_missions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_missions(db, skip=skip, limit=limit)

@app.put("/targets/{target_id}/notes", response_model=Target)
def update_target_notes(target_id: int, notes: str, db: Session = Depends(get_db)):
    db_target = crud.update_target_notes(db, target_id=target_id, notes=notes)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found or is already complete")
    return db_target

@app.put("/targets/{target_id}/complete", response_model=Target)
def mark_target_complete(target_id: int, db: Session = Depends(get_db)):
    db_target = crud.mark_target_complete(db, target_id=target_id)
    if db_target is None:
        raise HTTPException(status_code=404, detail="Target not found")
    return db_target

@app.delete("/missions/{mission_id}", response_model=Mission)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    db_mission = crud.delete_mission(db, mission_id=mission_id)
    if db_mission is None:
        raise HTTPException(status_code=404, detail="Mission not found or is assigned to a cat")
    return db_mission
