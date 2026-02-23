from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from app.config import get_config
import os

pages_router = APIRouter()

template = Jinja2Templates(directory=get_config().template_dir)

@pages_router.get('/')
def homepage_route():
 pass