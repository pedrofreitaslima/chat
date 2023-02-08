#!./venv/bin/python3
from fastapi import FastAPI, Request
import uvicorn
#from database.connection import Settings
from routes import routelist
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


#settings=Settings()
app=FastAPI()

app.mount("/static",StaticFiles(directory="static",html=True),name="static")
templates=Jinja2Templates(directory="views/")



#@app.on_event("startup")
#async def init_db():
#    await settings.initialize_database()

@app.get("/")
def root(request:Request)-> dict:
    return templates.TemplateResponse("login.html",
                                      {
                                          "request":request
                                      })
    
    
app.include_router(routelist.login_router,prefix="/login")    
    
    
if __name__ == "__main__":
 uvicorn.run("root:app", host="0.0.0.0", port=7654,reload=True)  