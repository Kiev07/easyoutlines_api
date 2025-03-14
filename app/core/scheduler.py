from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import FixedIncome as FixedIncomeModel, FixedExpense as FixedExpenseModel, UserMoney as UserMoneyModel

def update_fixed_incomes_and_expenses():
    db: Session = SessionLocal()
    try:
        now = datetime.utcnow()
        fixed_incomes = db.query(FixedIncomeModel).filter(FixedIncomeModel.status == "active").all()
        fixed_expenses = db.query(FixedExpenseModel).filter(FixedExpenseModel.status == "active").all()

        for income in fixed_incomes:
            if (now - income.updated_at).days >= income.frequency:
                user_money = db.query(UserMoneyModel).filter(UserMoneyModel.user_id == income.user_id).first()
                if user_money:
                    user_money.amount += income.amount
                    user_money.updated_at = now
                    income.updated_at = now
                    db.commit()

        for expense in fixed_expenses:
            if (now - expense.updated_at).days >= expense.frequency:
                user_money = db.query(UserMoneyModel).filter(UserMoneyModel.user_id == expense.user_id).first()
                if user_money:
                    user_money.amount -= expense.amount
                    user_money.updated_at = now
                    expense.updated_at = now
                    db.commit()
    finally:
        db.close()

scheduler = BackgroundScheduler()
scheduler.add_job(update_fixed_incomes_and_expenses, 'interval', days=1)
scheduler.start()