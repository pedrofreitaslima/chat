from typing import List
from beanie import PydanticObjectId
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Path, HTTPException, status, Request, Depends


login_router = APIRouter(tags=["Login"])
templates = Jinja2Templates(directory="views/")


@login_router.get("/")
def retrieve_login(request: Request):
  return templates.TemplateResponse("login.html",
    {
      "request": request
    })
