from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import datetime
from ..database import get_db
from ..models import (
    FixedIncome as FixedIncomeModel,
    VariableIncome as VariableIncomeModel,
    FixedExpense as FixedExpenseModel,
    VariableExpense as VariableExpenseModel,
    Saving as SavingModel,
    Debt as DebtModel,
    Goal as GoalModel,
    FixedInvestment as FixedInvestmentModel,
    VariableInvestment as VariableInvestmentModel,
)

router = APIRouter()

def calculate_trend(data):
    x = np.array([i for i in range(len(data))]).reshape(-1, 1)  # Índices como variable independiente
    y = np.array(data).reshape(-1, 1)  # Valores como variable dependiente

    model = LinearRegression()
    model.fit(x, y)

    m = model.coef_[0][0]  # Pendiente
    b = model.intercept_[0]  # Intersección
    return f"y = {m:.2f}x + {b:.2f}"

@router.get("/analysis/{table_name}")
def analyze_table(table_name: str, db: Session = Depends(get_db)):
    table_mapping = {
        "fixed_incomes": FixedIncomeModel,
        "variable_incomes": VariableIncomeModel,
        "fixed_expenses": FixedExpenseModel,
        "variable_expenses": VariableExpenseModel,
        "savings": SavingModel,
        "debts": DebtModel,
        "goals": GoalModel,
        "fixed_investments": FixedInvestmentModel,
        "variable_investments": VariableInvestmentModel,
    }

    if table_name not in table_mapping:
        raise HTTPException(status_code=400, detail="Tabla no válida para análisis")

    model = table_mapping[table_name]
    records = db.query(model).filter(model.status == "active").order_by(model.created_at).all()

    if len(records) < 10:
        raise HTTPException(
            status_code=422,
            detail="Se requieren al menos 10 registros para calcular la tendencia"
        )

    if hasattr(model, "amount"):
        data = [record.amount for record in records]
    else:
        raise HTTPException(
            status_code=400,
            detail="La tabla no tiene un campo 'amount' para analizar"
        )

    trend_equation = calculate_trend(data)
    return {"table": table_name, "trend_equation": trend_equation}