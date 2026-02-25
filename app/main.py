from fastapi import FastAPI,Request,APIRouter
from fastapi.staticfiles import StaticFiles
from app.api.file_route import files_router
from app.api.auth_route import auth_router
from app.pages.pages_routes import pages_router
from app.api.user_route import user_router
from app.utils.exceptions import ServiceException
from app.utils.response import make_response
from app.config import get_config

import traceback


app = FastAPI()

@app.exception_handler(ServiceException)
async def handle_service_exception(request:Request,exc:ServiceException):
    traceback.print_exception(exc)
    return make_response({
        "success":False,
        "code":exc.code,
        "data":exc.data
    })

app.mount("/static",StaticFiles(directory=get_config().static_dir),name="static")

api_router = APIRouter(prefix="/api")

api_router.include_router(
    files_router,
    prefix="/file"
)
api_router.include_router(
    auth_router,
    prefix="/auth"
)
api_router.include_router(
    user_router,
    prefix="/user"
)
app.include_router(
    pages_router
)

app.include_router(api_router)