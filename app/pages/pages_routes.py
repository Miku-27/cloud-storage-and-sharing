from fastapi import APIRouter,Request
from fastapi.templating import Jinja2Templates
from app.config import get_config
import os

pages_router = APIRouter()

template = Jinja2Templates(directory=get_config().template_dir)

@pages_router.get('/')
def homepage_route(request:Request):
    return template.TemplateResponse("index.html",{'request':request})

@pages_router.get('/login')
def homepage_route(request:Request):
    return template.TemplateResponse("login.html",{'request':request})

@pages_router.get('/register')
def homepage_route(request:Request):
    return template.TemplateResponse("register.html",{'request':request})