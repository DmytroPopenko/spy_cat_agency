from sqlalchemy.orm import Session
from models import SpyCat, Mission, Target
from schemas import SpyCatCreate, MissionCreate, TargetCreate
from utils import validate_cat_breed


def create_spycat(db: Session, spycat: SpyCatCreate):      
    db_spycat = SpyCat()
    db_spycat.name=spycat.name
    db_spycat.experience_years=spycat.experience_years
    db_spycat.breed=spycat.breed
    db_spycat.salary=spycat.salary
    db.add(db_spycat)
    db.commit()
    db.refresh(db_spycat)
    return db_spycat


def get_spycat(db: Session, spycat_id: int):
    return db.query(SpyCat).filter(SpyCat.id == spycat_id).first()

def get_spycats(db: Session, skip: int = 0, limit: int = 10):
    return db.query(SpyCat).offset(skip).limit(limit).all()

def update_spycat_salary(db: Session, spycat_id: int, new_salary: float):
    db_spycat = get_spycat(db, spycat_id)
    if db_spycat:
        db_spycat.salary = new_salary
        db.commit()
        db.refresh(db_spycat)
    return db_spycat

def delete_spycat(db: Session, spycat_id: int):
    db_spycat = get_spycat(db, spycat_id)
    if db_spycat:
        db.delete(db_spycat)
        db.commit()
    return db_spycat

def create_mission(db: Session, mission_data: MissionCreate, cat_id: int):
    db_mission = Mission(cat_id=cat_id, is_complete=False)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)

    for target_data in mission_data.targets:
        db_target = Target(**target_data.dict(), mission_id=db_mission.id)
        db.add(db_target)
    db.commit()
    return db_mission

def get_mission(db: Session, mission_id: int):
    return db.query(Mission).filter(Mission.id == mission_id).first()

def get_missions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Mission).offset(skip).limit(limit).all()

def update_target_notes(db: Session, target_id: int, notes: str):
    db_target = db.query(Target).filter(Target.id == target_id, Target.is_complete == False).first()
    if db_target:
        db_target.notes = notes
        db.commit()
        db.refresh(db_target)
    return db_target

def mark_target_complete(db: Session, target_id: int):
    db_target = db.query(Target).filter(Target.id == target_id).first()
    if db_target:
        db_target.is_complete = True
        db.commit()
        db.refresh(db_target)

        mission = db_target.mission
        if all(target.is_complete for target in mission.targets):
            mission.is_complete = True
            db.commit()
            db.refresh(mission)
    return db_target

def delete_mission(db: Session, mission_id: int):
    db_mission = get_mission(db, mission_id)
    if db_mission and not db_mission.cat_id:
        db.delete(db_mission)
        db.commit()
    return db_mission
