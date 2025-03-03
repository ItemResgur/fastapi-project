from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Подключаем папку html как статическую для CSS
app.mount("/static", StaticFiles(directory="html"), name="static")

# Указываем папку html для шаблонов
templates = Jinja2Templates(directory="html")

# Настройка базы данных
DATABASE_URL = "sqlite:///./greetings.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Greeting(Base):
    __tablename__ = "greetings"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    message = Column(Text)

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send_greeting/")
async def send_greeting(name: str = Form(...), message: str = Form(...)):
    db = SessionLocal()
    greeting = Greeting(name=name, message=message)
    db.add(greeting)
    db.commit()
    db.refresh(greeting)
    db.close()
    return {"message": "Greeting sent successfully!"}

@app.get("/greetings/", response_class=HTMLResponse)
async def get_greetings(request: Request):
    db = SessionLocal()
    greetings = db.query(Greeting).all()
    db.close()
    return templates.TemplateResponse("greetings.html", {"request": request, "greetings": greetings})

@app.get("/api/greetings/")
async def api_get_greetings():
    db = SessionLocal()
    greetings = db.query(Greeting).all()
    db.close()
    return [{"name": greeting.name, "message": greeting.message} for greeting in greetings]

@app.post("/api/send_greeting/")
async def api_send_greeting(name: str = Form(...), message: str = Form(...)):
    db = SessionLocal()
    greeting = Greeting(name=name, message=message)
    db.add(greeting)
    db.commit()
    db.refresh(greeting)
    db.close()
    return {"message": "Greeting sent successfully!"}