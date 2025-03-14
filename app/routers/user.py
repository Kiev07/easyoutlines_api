from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from ..database import get_db
from ..models import User, FixedIncome as FixedIncomeModel, VariableIncome as VariableIncomeModel, FixedExpense as FixedExpenseModel, VariableExpense as VariableExpenseModel, Saving as SavingModel, Debt as DebtModel, Goal as GoalModel, FixedInvestment as FixedInvestmentModel, VariableInvestment as VariableInvestmentModel, UserMoney as UserMoneyModel
from ..routers.auth import get_current_user
from ..pydantic_models import FixedIncome, VariableIncome, FixedExpense, VariableExpense, Saving, Debt, Goal, FixedInvestment, VariableInvestment, UserMoney, UserMovements

router = APIRouter()

def create_user_movement(db: Session, user_id: int, description: str):
    movement = UserMovements(
        user_id=user_id,
        description=description,
        created_at=datetime.utcnow()
    )
    db.add(movement)
    db.commit()
    db.refresh(movement)

class FixedIncomeCreate(BaseModel):
    name: str
    amount: float
    frequency: int
    status: str = "active"

class VariableIncomeCreate(BaseModel):
    name: str
    amount: float
    received_date: datetime
    status: str = "active"

class FixedExpenseCreate(BaseModel):
    name: str
    amount: float
    frequency: int
    status: str = "active"

class VariableExpenseCreate(BaseModel):
    name: str
    amount: float
    paid_date: datetime
    status: str = "active"

class SavingCreate(BaseModel):
    name: str
    amount: float
    status: str = "active"

class DebtCreate(BaseModel):
    name: str
    amount: float
    payment: float
    interest_rate: float
    interest_type: str
    interest_period_days: int
    interest_free_months: int
    status: str = "active"

class GoalCreate(BaseModel):
    name: str
    amount: float
    saved_amount: float
    status: str = "active"

class FixedInvestmentCreate(BaseModel):
    name: str
    amount: float
    interest_rate: float
    interest_type: str
    interest_period_days: int
    status: str = "active"

class VariableInvestmentCreate(BaseModel):
    name: str
    amount: float
    interest_rate: float
    interest_type: str
    interest_period_days: int
    start_date: datetime
    end_date: datetime
    status: str = "active"

class UserMoneyCreate(BaseModel):
    amount: float
    status: str = "active"

@router.get("/fixed_incomes", response_model=List[FixedIncome])
def get_fixed_incomes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(FixedIncomeModel).filter(FixedIncomeModel.user_id == current_user.user_id, FixedIncomeModel.status == "active").all()

@router.post("/fixed_incomes", response_model=FixedIncome)
def create_fixed_income(fixed_income: FixedIncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_fixed_income = FixedIncomeModel(
        user_id=current_user.user_id,
        name=fixed_income.name,
        amount=fixed_income.amount,
        frequency=fixed_income.frequency,
        status=fixed_income.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_fixed_income)
    db.commit()
    db.refresh(new_fixed_income)
    create_user_movement(db, current_user.user_id, f"Created fixed income: {fixed_income.name}")
    return new_fixed_income

@router.put("/fixed_incomes/{fixed_income_id}", response_model=FixedIncome)
def update_fixed_income(fixed_income_id: int, fixed_income: FixedIncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_income = db.query(FixedIncomeModel).filter(FixedIncomeModel.fixed_income_id == fixed_income_id).first()
    if not db_fixed_income:
        raise HTTPException(status_code=404, detail="Fixed income not found")
    db_fixed_income.name = fixed_income.name
    db_fixed_income.amount = fixed_income.amount
    db_fixed_income.frequency = fixed_income.frequency
    db_fixed_income.status = fixed_income.status
    db_fixed_income.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_income)
    create_user_movement(db, current_user.user_id, f"Updated fixed income: {fixed_income.name}")
    return db_fixed_income

@router.delete("/fixed_incomes/{fixed_income_id}", response_model=FixedIncome)
def delete_fixed_income(fixed_income_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_income = db.query(FixedIncomeModel).filter(FixedIncomeModel.fixed_income_id == fixed_income_id).first()
    if not db_fixed_income:
        raise HTTPException(status_code=404, detail="Fixed income not found")
    db_fixed_income.status = "inactive"
    db_fixed_income.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_income)
    create_user_movement(db, current_user.user_id, f"Deleted fixed income: {db_fixed_income.name}")
    return db_fixed_income

# Repite el mismo patrón para las demás tablas (VariableIncome, FixedExpense, VariableExpense, Saving, Debt, Goal, FixedInvestment, VariableInvestment, UserMoney)

@router.get("/variable_incomes", response_model=List[VariableIncome])
def get_variable_incomes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(VariableIncomeModel).filter(VariableIncomeModel.user_id == current_user.user_id, VariableIncomeModel.status == "active").all()

@router.post("/variable_incomes", response_model=VariableIncome)
def create_variable_income(variable_income: VariableIncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_variable_income = VariableIncomeModel(
        user_id=current_user.user_id,
        name=variable_income.name,
        amount=variable_income.amount,
        received_date=variable_income.received_date,
        status=variable_income.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_variable_income)
    db.commit()
    db.refresh(new_variable_income)
    create_user_movement(db, current_user.user_id, f"Created variable income: {variable_income.name}")
    return new_variable_income

@router.put("/variable_incomes/{variable_income_id}", response_model=VariableIncome)
def update_variable_income(variable_income_id: int, variable_income: VariableIncomeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_income = db.query(VariableIncomeModel).filter(VariableIncomeModel.variable_income_id == variable_income_id).first()
    if not db_variable_income:
        raise HTTPException(status_code=404, detail="Variable income not found")
    db_variable_income.name = variable_income.name
    db_variable_income.amount = variable_income.amount
    db_variable_income.received_date = variable_income.received_date
    db_variable_income.status = variable_income.status
    db_variable_income.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_income)
    create_user_movement(db, current_user.user_id, f"Updated variable income: {variable_income.name}")
    return db_variable_income

@router.delete("/variable_incomes/{variable_income_id}", response_model=VariableIncome)
def delete_variable_income(variable_income_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_income = db.query(VariableIncomeModel).filter(VariableIncomeModel.variable_income_id == variable_income_id).first()
    if not db_variable_income:
        raise HTTPException(status_code=404, detail="Variable income not found")
    db_variable_income.status = "inactive"
    db_variable_income.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_income)
    create_user_movement(db, current_user.user_id, f"Deleted variable income: {db_variable_income.name}")
    return db_variable_income

@router.get("/fixed_expenses", response_model=List[FixedExpense])
def get_fixed_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(FixedExpenseModel).filter(FixedExpenseModel.user_id == current_user.user_id, FixedExpenseModel.status == "active").all()

@router.post("/fixed_expenses", response_model=FixedExpense)
def create_fixed_expense(fixed_expense: FixedExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_fixed_expense = FixedExpenseModel(
        user_id=current_user.user_id,
        name=fixed_expense.name,
        amount=fixed_expense.amount,
        frequency=fixed_expense.frequency,
        status=fixed_expense.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_fixed_expense)
    db.commit()
    db.refresh(new_fixed_expense)
    create_user_movement(db, current_user.user_id, f"Created fixed expense: {fixed_expense.name}")
    return new_fixed_expense

@router.put("/fixed_expenses/{fixed_expense_id}", response_model=FixedExpense)
def update_fixed_expense(fixed_expense_id: int, fixed_expense: FixedExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_expense = db.query(FixedExpenseModel).filter(FixedExpenseModel.fixed_expense_id == fixed_expense_id).first()
    if not db_fixed_expense:
        raise HTTPException(status_code=404, detail="Fixed expense not found")
    db_fixed_expense.name = fixed_expense.name
    db_fixed_expense.amount = fixed_expense.amount
    db_fixed_expense.frequency = fixed_expense.frequency
    db_fixed_expense.status = fixed_expense.status
    db_fixed_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_expense)
    create_user_movement(db, current_user.user_id, f"Updated fixed expense: {fixed_expense.name}")
    return db_fixed_expense

@router.delete("/fixed_expenses/{fixed_expense_id}", response_model=FixedExpense)
def delete_fixed_expense(fixed_expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_expense = db.query(FixedExpenseModel).filter(FixedExpenseModel.fixed_expense_id == fixed_expense_id).first()
    if not db_fixed_expense:
        raise HTTPException(status_code=404, detail="Fixed expense not found")
    db_fixed_expense.status = "inactive"
    db_fixed_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_expense)
    create_user_movement(db, current_user.user_id, f"Deleted fixed expense: {db_fixed_expense.name}")
    return db_fixed_expense

@router.get("/variable_expenses", response_model=List[VariableExpense])
def get_variable_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(VariableExpenseModel).filter(VariableExpenseModel.user_id == current_user.user_id, VariableExpenseModel.status == "active").all()

@router.post("/variable_expenses", response_model=VariableExpense)
def create_variable_expense(variable_expense: VariableExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_variable_expense = VariableExpenseModel(
        user_id=current_user.user_id,
        name=variable_expense.name,
        amount=variable_expense.amount,
        paid_date=variable_expense.paid_date,
        status=variable_expense.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_variable_expense)
    db.commit()
    db.refresh(new_variable_expense)
    create_user_movement(db, current_user.user_id, f"Created variable expense: {variable_expense.name}")
    return new_variable_expense

@router.put("/variable_expenses/{variable_expense_id}", response_model=VariableExpense)
def update_variable_expense(variable_expense_id: int, variable_expense: VariableExpenseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_expense = db.query(VariableExpenseModel).filter(VariableExpenseModel.variable_expense_id == variable_expense_id).first()
    if not db_variable_expense:
        raise HTTPException(status_code=404, detail="Variable expense not found")
    db_variable_expense.name = variable_expense.name
    db_variable_expense.amount = variable_expense.amount
    db_variable_expense.paid_date = variable_expense.paid_date
    db_variable_expense.status = variable_expense.status
    db_variable_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_expense)
    create_user_movement(db, current_user.user_id, f"Updated variable expense: {variable_expense.name}")
    return db_variable_expense

@router.delete("/variable_expenses/{variable_expense_id}", response_model=VariableExpense)
def delete_variable_expense(variable_expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_expense = db.query(VariableExpenseModel).filter(VariableExpenseModel.variable_expense_id == variable_expense_id).first()
    if not db_variable_expense:
        raise HTTPException(status_code=404, detail="Variable expense not found")
    db_variable_expense.status = "inactive"
    db_variable_expense.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_expense)
    create_user_movement(db, current_user.user_id, f"Deleted variable expense: {db_variable_expense.name}")
    return db_variable_expense

@router.get("/savings", response_model=List[Saving])
def get_savings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(SavingModel).filter(SavingModel.user_id == current_user.user_id, SavingModel.status == "active").all()

@router.post("/savings", response_model=Saving)
def create_saving(saving: SavingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_saving = SavingModel(
        user_id=current_user.user_id,
        name=saving.name,
        amount=saving.amount,
        status=saving.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_saving)
    db.commit()
    db.refresh(new_saving)
    create_user_movement(db, current_user.user_id, f"Created saving: {saving.name}")
    return new_saving

@router.put("/savings/{saving_id}", response_model=Saving)
def update_saving(saving_id: int, saving: SavingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_saving = db.query(SavingModel).filter(SavingModel.saving_id == saving_id).first()
    if not db_saving:
        raise HTTPException(status_code=404, detail="Saving not found")
    db_saving.name = saving.name
    db_saving.amount = saving.amount
    db_saving.status = saving.status
    db_saving.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_saving)
    create_user_movement(db, current_user.user_id, f"Updated saving: {saving.name}")
    return db_saving

@router.delete("/savings/{saving_id}", response_model=Saving)
def delete_saving(saving_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_saving = db.query(SavingModel).filter(SavingModel.saving_id == saving_id).first()
    if not db_saving:
        raise HTTPException(status_code=404, detail="Saving not found")
    db_saving.status = "inactive"
    db_saving.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_saving)
    create_user_movement(db, current_user.user_id, f"Deleted saving: {db_saving.name}")
    return db_saving

@router.get("/debts", response_model=List[Debt])
def get_debts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(DebtModel).filter(DebtModel.user_id == current_user.user_id, DebtModel.status == "active").all()

@router.post("/debts", response_model=Debt)
def create_debt(debt: DebtCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_debt = DebtModel(
        user_id=current_user.user_id,
        name=debt.name,
        amount=debt.amount,
        payment=debt.payment,
        interest_rate=debt.interest_rate,
        interest_type=debt.interest_type,
        interest_period_days=debt.interest_period_days,
        interest_free_months=debt.interest_free_months,
        status=debt.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_debt)
    db.commit()
    db.refresh(new_debt)
    create_user_movement(db, current_user.user_id, f"Created debt: {debt.name}")
    return new_debt

@router.put("/debts/{debt_id}", response_model=Debt)
def update_debt(debt_id: int, debt: DebtCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_debt = db.query(DebtModel).filter(DebtModel.debt_id == debt_id).first()
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    db_debt.name = debt.name
    db_debt.amount = debt.amount
    db_debt.payment = debt.payment
    db_debt.interest_rate = debt.interest_rate
    db_debt.interest_type = debt.interest_type
    db_debt.interest_period_days = debt.interest_period_days
    db_debt.interest_free_months = debt.interest_free_months
    db_debt.status = debt.status
    db_debt.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_debt)
    create_user_movement(db, current_user.user_id, f"Updated debt: {debt.name}")
    return db_debt

@router.delete("/debts/{debt_id}", response_model=Debt)
def delete_debt(debt_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_debt = db.query(DebtModel).filter(DebtModel.debt_id == debt_id).first()
    if not db_debt:
        raise HTTPException(status_code=404, detail="Debt not found")
    db_debt.status = "inactive"
    db_debt.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_debt)
    create_user_movement(db, current_user.user_id, f"Deleted debt: {db_debt.name}")
    return db_debt

@router.get("/goals", response_model=List[Goal])
def get_goals(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(GoalModel).filter(GoalModel.user_id == current_user.user_id, GoalModel.status == "active").all()

@router.post("/goals", response_model=Goal)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_goal = GoalModel(
        user_id=current_user.user_id,
        name=goal.name,
        amount=goal.amount,
        saved_amount=goal.saved_amount,
        status=goal.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)
    create_user_movement(db, current_user.user_id, f"Created goal: {goal.name}")
    return new_goal

@router.put("/goals/{goal_id}", response_model=Goal)
def update_goal(goal_id: int, goal: GoalCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_goal = db.query(GoalModel).filter(GoalModel.goal_id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db_goal.name = goal.name
    db_goal.amount = goal.amount
    db_goal.saved_amount = goal.saved_amount
    db_goal.status = goal.status
    db_goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_goal)
    create_user_movement(db, current_user.user_id, f"Updated goal: {goal.name}")
    return db_goal

@router.delete("/goals/{goal_id}", response_model=Goal)
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_goal = db.query(GoalModel).filter(GoalModel.goal_id == goal_id).first()
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    db_goal.status = "inactive"
    db_goal.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_goal)
    create_user_movement(db, current_user.user_id, f"Deleted goal: {db_goal.name}")
    return db_goal

@router.get("/fixed_investments", response_model=List[FixedInvestment])
def get_fixed_investments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(FixedInvestmentModel).filter(FixedInvestmentModel.user_id == current_user.user_id, FixedInvestmentModel.status == "active").all()

@router.post("/fixed_investments", response_model=FixedInvestment)
def create_fixed_investment(fixed_investment: FixedInvestmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_fixed_investment = FixedInvestmentModel(
        user_id=current_user.user_id,
        name=fixed_investment.name,
        amount=fixed_investment.amount,
        interest_rate=fixed_investment.interest_rate,
        interest_type=fixed_investment.interest_type,
        interest_period_days=fixed_investment.interest_period_days,
        status=fixed_investment.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_fixed_investment)
    db.commit()
    db.refresh(new_fixed_investment)
    create_user_movement(db, current_user.user_id, f"Created fixed investment: {fixed_investment.name}")
    return new_fixed_investment

@router.put("/fixed_investments/{fixed_investment_id}", response_model=FixedInvestment)
def update_fixed_investment(fixed_investment_id: int, fixed_investment: FixedInvestmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_investment = db.query(FixedInvestmentModel).filter(FixedInvestmentModel.fixed_investment_id == fixed_investment_id).first()
    if not db_fixed_investment:
        raise HTTPException(status_code=404, detail="Fixed investment not found")
    db_fixed_investment.name = fixed_investment.name
    db_fixed_investment.amount = fixed_investment.amount
    db_fixed_investment.interest_rate = fixed_investment.interest_rate
    db_fixed_investment.interest_type = fixed_investment.interest_type
    db_fixed_investment.interest_period_days = fixed_investment.interest_period_days
    db_fixed_investment.status = fixed_investment.status
    db_fixed_investment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_investment)
    create_user_movement(db, current_user.user_id, f"Updated fixed investment: {fixed_investment.name}")
    return db_fixed_investment

@router.delete("/fixed_investments/{fixed_investment_id}", response_model=FixedInvestment)
def delete_fixed_investment(fixed_investment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_fixed_investment = db.query(FixedInvestmentModel).filter(FixedInvestmentModel.fixed_investment_id == fixed_investment_id).first()
    if not db_fixed_investment:
        raise HTTPException(status_code=404, detail="Fixed investment not found")
    db_fixed_investment.status = "inactive"
    db_fixed_investment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_fixed_investment)
    create_user_movement(db, current_user.user_id, f"Deleted fixed investment: {db_fixed_investment.name}")
    return db_fixed_investment

@router.get("/variable_investments", response_model=List[VariableInvestment])
def get_variable_investments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(VariableInvestmentModel).filter(VariableInvestmentModel.user_id == current_user.user_id, VariableInvestmentModel.status == "active").all()

@router.post("/variable_investments", response_model=VariableInvestment)
def create_variable_investment(variable_investment: VariableInvestmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_variable_investment = VariableInvestmentModel(
        user_id=current_user.user_id,
        name=variable_investment.name,
        amount=variable_investment.amount,
        interest_rate=variable_investment.interest_rate,
        interest_type=variable_investment.interest_type,
        interest_period_days=variable_investment.interest_period_days,
        start_date=variable_investment.start_date,
        end_date=variable_investment.end_date,
        status=variable_investment.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_variable_investment)
    db.commit()
    db.refresh(new_variable_investment)
    create_user_movement(db, current_user.user_id, f"Created variable investment: {variable_investment.name}")
    return new_variable_investment

@router.put("/variable_investments/{variable_investment_id}", response_model=VariableInvestment)
def update_variable_investment(variable_investment_id: int, variable_investment: VariableInvestmentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_investment = db.query(VariableInvestmentModel).filter(VariableInvestmentModel.variable_investment_id == variable_investment_id).first()
    if not db_variable_investment:
        raise HTTPException(status_code=404, detail="Variable investment not found")
    db_variable_investment.name = variable_investment.name
    db_variable_investment.amount = variable_investment.amount
    db_variable_investment.interest_rate = variable_investment.interest_rate
    db_variable_investment.interest_type = variable_investment.interest_type
    db_variable_investment.interest_period_days = variable_investment.interest_period_days
    db_variable_investment.start_date = variable_investment.start_date
    db_variable_investment.end_date = variable_investment.end_date
    db_variable_investment.status = variable_investment.status
    db_variable_investment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_investment)
    create_user_movement(db, current_user.user_id, f"Updated variable investment: {variable_investment.name}")
    return db_variable_investment

@router.delete("/variable_investments/{variable_investment_id}", response_model=VariableInvestment)
def delete_variable_investment(variable_investment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_variable_investment = db.query(VariableInvestmentModel).filter(VariableInvestmentModel.variable_investment_id == variable_investment_id).first()
    if not db_variable_investment:
        raise HTTPException(status_code=404, detail="Variable investment not found")
    db_variable_investment.status = "inactive"
    db_variable_investment.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_variable_investment)
    create_user_movement(db, current_user.user_id, f"Deleted variable investment: {db_variable_investment.name}")
    return db_variable_investment

@router.get("/user_money", response_model=UserMoney)
def get_user_money(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(UserMoneyModel).filter(UserMoneyModel.user_id == current_user.user_id, UserMoneyModel.status == "active").first()

@router.post("/user_money", response_model=UserMoney)
def create_user_money(user_money: UserMoneyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_user_money = UserMoneyModel(
        user_id=current_user.user_id,
        amount=user_money.amount,
        status=user_money.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_user_money)
    db.commit()
    db.refresh(new_user_money)
    create_user_movement(db, current_user.user_id, f"Created user money")
    return new_user_money

@router.put("/user_money", response_model=UserMoney)
def update_user_money(user_money: UserMoneyCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user_money = db.query(UserMoneyModel).filter(UserMoneyModel.user_id == current_user.user_id).first()
    if not db_user_money:
        raise HTTPException(status_code=404, detail="User money not found")
    db_user_money.amount = user_money.amount
    db_user_money.status = user_money.status
    db_user_money.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user_money)
    create_user_movement(db, current_user.user_id, f"Updated user money")
    return db_user_money

@router.delete("/user_money", response_model=UserMoney)
def delete_user_money(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user_money = db.query(UserMoneyModel).filter(UserMoneyModel.user_id == current_user.user_id).first()
    if not db_user_money:
        raise HTTPException(status_code=404, detail="User money not found")
    db_user_money.status = "inactive"
    db_user_money.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user_money)
    create_user_movement(db, current_user.user_id, f"Deleted user money")
    return db_user_money