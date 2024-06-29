from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")


users: set[str] = {""}

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


# route: /get_friends
@app.get("/get_users")
def get_users(request: Request):
    return templates.TemplateResponse("get_users.html", {"request": request, "users": list(users)})


# route: /add_user
@app.route("/add_user", methods=["GET", "POST"])
async def add_user(request: Request):
    if request.method == "POST":
        data = await request.json()
        name = data.get("name")
        users.add(name)
        return JSONResponse(content={"message": f"Hello, {name}!"})
    return templates.TemplateResponse("add_user.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
