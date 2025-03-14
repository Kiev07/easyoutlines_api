from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str
    status: str
    created_at: datetime
    updated_at: datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str = "user"

class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserMovements(BaseModel):
    user_id: int
    description: str
    created_at: datetime

class FixedIncome(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    frequency: int
    status: str
    created_at: datetime
    updated_at: datetime

class VariableIncome(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    received_date: date
    status: str
    created_at: datetime
    updated_at: datetime

class FixedExpense(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    frequency: int
    status: str
    created_at: datetime
    updated_at: datetime

class VariableExpense(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    paid_date: date
    status: str
    created_at: datetime
    updated_at: datetime

class Saving(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

class Debt(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    payment: Decimal
    interest_rate: Decimal
    interest_type: str
    interest_period_days: int
    interest_free_months: int
    status: str
    created_at: datetime
    updated_at: datetime

class Goal(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    saved_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

class FixedInvestment(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    interest_rate: Decimal
    interest_type: str
    interest_period_days: int
    status: str
    created_at: datetime
    updated_at: datetime

class VariableInvestment(BaseModel):
    user_id: int
    name: str
    amount: Decimal
    interest_rate: Decimal
    interest_type: str
    interest_period_days: int
    start_date: date
    end_date: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime

class UserMoney(BaseModel):
    user_id: int
    amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    status: str
    created_at: datetime
    updated_at: datetime