from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SQLALCHEMY_DATABASE_URL = "sqlite:///./database/users.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


Base.metadata.create_all(bind=engine)

db = SessionLocal()


@app.on_event("startup")
def startup():
    def shutdown_session():
        db.close()

    app.add_event_handler("shutdown", shutdown_session)


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@app.get("/get_users")
def get_users(request: Request):
    users = db.query(User).all()
    return templates.TemplateResponse("get_users.html", {"request": request, "users": users})


@app.route("/add_user", methods=["GET", "POST"])
async def add_user(request: Request):
    if request.method == "POST":
        data = await request.json()
        name = data.get("name")
        if db.query(User).filter(User.name == name).first():
            return JSONResponse(content={"message": f"User {name} already exists!"}, status_code=400)
        new_user = User(name=name)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return JSONResponse(content={"message": f"User {name} added with ID {new_user.id}"})
    return templates.TemplateResponse("add_user.html", {"request": request})


app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

# TODO: create a route to add friend request by name or id form database

# TODO: create a route to list friends request, accept or dismiss requests

# TODO: create a route to view list all friends and delete friends

# TODO: fixed all deprecated method in codes
