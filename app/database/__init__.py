from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .base import Base
from sqlalchemy.exc import IntegrityError
from ..models import User
from ..core.security import hash_password
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

URI_DATABASE = os.getenv("URI_DATABASE")

engine = create_engine(URI_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)

    # Crear usuario administrador si no existe
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter_by(email="admin").first()
        if not admin_user:
            admin_user = User(
                first_name="Admin",
                last_name="User",
                email="admin@easyoutlays.com",
                password=hash_password("admin"),  # Hashea la contraseña
                role="admin",
                status="active",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created")
    except IntegrityError:
        db.rollback()
    finally:
        db.close()