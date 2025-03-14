from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, TIMESTAMP, DATE

from ..database.base import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class UserMovements(Base):
    __tablename__ = 'user_movements'
    movement_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)

class FixedIncome(Base):
    __tablename__ = 'fixed_incomes'
    fixed_income_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    frequency = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class VariableIncome(Base):
    __tablename__ = 'variable_incomes'
    variable_income_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    received_date = Column(DATE, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class FixedExpense(Base):
    __tablename__ = 'fixed_expenses'
    fixed_expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    frequency = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class VariableExpense(Base):
    __tablename__ = 'variable_expenses'
    variable_expense_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    paid_date = Column(DATE, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class Saving(Base):
    __tablename__ = 'savings'
    saving_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class Debt(Base):
    __tablename__ = 'debts'
    debt_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    payment = Column(DECIMAL(10, 2), nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    interest_type = Column(String(255), nullable=False)
    interest_period_days = Column(Integer, nullable=False)
    interest_free_months = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class Goal(Base):
    __tablename__ = 'goals'
    goal_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    saved_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class FixedInvestment(Base):
    __tablename__ = 'fixed_investments'
    fixed_investment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    interest_type = Column(String(255), nullable=False)
    interest_period_days = Column(Integer, nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class VariableInvestment(Base):
    __tablename__ = 'variable_investments'
    variable_investment_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(255), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    interest_rate = Column(DECIMAL(5, 2), nullable=False)
    interest_type = Column(String(255), nullable=False)
    interest_period_days = Column(Integer, nullable=False)
    start_date = Column(DATE, nullable=False)
    end_date = Column(DATE, nullable=True)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class UserMoney(Base):
    __tablename__ = 'user_money'
    user_money_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)