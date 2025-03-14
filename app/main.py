from fastapi import FastAPI
from app.database import SessionLocal, init_db
from app.routers import auth, user, admin
from app.core.scheduler import scheduler

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def on_startup():
    init_db()
    if not scheduler.running:
        scheduler.start()

@app.on_event("shutdown")
def on_shutdown():
    if scheduler.running:
        scheduler.shutdown()

@app.get("/")
async def read_root():
    return {"message": "Hola mundo"}

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=8000, reload=True)