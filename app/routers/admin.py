from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import User as UserModel, FixedIncome as FixedIncomeModel, VariableIncome as VariableIncomeModel, FixedExpense as FixedExpenseModel, VariableExpense as VariableExpenseModel, Saving as SavingModel, Debt as DebtModel, Goal as GoalModel, FixedInvestment as FixedInvestmentModel, VariableInvestment as VariableInvestmentModel, UserMoney as UserMoneyModel
from ..core.security import hash_password
from ..routers.auth import get_admin_user
from ..pydantic_models import User, UserCreate, UserUpdate, UserResponse

router = APIRouter()

def inactivate_records(db: Session, model, user_id: int):
    records = db.query(model).filter(model.user_id == user_id).all()
    for record in records:
        record.status = "inactive"
        record.updated_at = datetime.utcnow()
    db.commit()

def reactivate_records(db: Session, model, user_id: int):
    records = db.query(model).filter(model.user_id == user_id).all()
    for record in records:
        record.status = "active"
        record.updated_at = datetime.utcnow()
    db.commit()

@router.get("/users", response_model=List[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    users = db.query(UserModel).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="err_user_not_found")
    return db_user

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="err_email_already_registered")
    hashed_password = hash_password(user.password)
    new_user = UserModel(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        status="active",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="err_user_not_found")
    db_user.first_name = user.first_name
    db_user.last_name = user.last_name
    db_user.email = user.email
    db_user.role = user.role
    db_user.status = user.status
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="err_user_not_found")
    
    if current_user.user_id == user_id and current_user.role == "admin":
        raise HTTPException(status_code=401, detail= "err_admin_cannot_delete_self")

    inactivate_records(db, FixedIncomeModel, user_id)
    inactivate_records(db, VariableIncomeModel, user_id)
    inactivate_records(db, FixedExpenseModel, user_id)
    inactivate_records(db, VariableExpenseModel, user_id)
    inactivate_records(db, SavingModel, user_id)
    inactivate_records(db, DebtModel, user_id)
    inactivate_records(db, GoalModel, user_id)
    inactivate_records(db, FixedInvestmentModel, user_id)
    inactivate_records(db, VariableInvestmentModel, user_id)
    inactivate_records(db, UserMoneyModel, user_id)

    db_user.status = "inactive"
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return {"message": "OK"}

@router.put("/users/{user_id}/reactivate", response_model=User)
def reactivate_user(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="err_user_not_found")
    
    reactivate_records(db, FixedIncomeModel, user_id)
    reactivate_records(db, VariableIncomeModel, user_id)
    reactivate_records(db, FixedExpenseModel, user_id)
    reactivate_records(db, VariableExpenseModel, user_id)
    reactivate_records(db, SavingModel, user_id)
    reactivate_records(db, DebtModel, user_id)
    reactivate_records(db, GoalModel, user_id)
    reactivate_records(db, FixedInvestmentModel, user_id)
    reactivate_records(db, VariableInvestmentModel, user_id)
    reactivate_records(db, UserMoneyModel, user_id)

    db_user.status = "active"
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user