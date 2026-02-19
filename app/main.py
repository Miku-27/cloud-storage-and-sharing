from fastapi import FastAPI,Request
from app.api.file_route import files_router
from app.api.auth_route import auth_router
from app.utils.exceptions import ServiceException
from app.utils.response import make_response

app = FastAPI()

@app.exception_handler(ServiceException)
async def handle_service_exception(request:Request,exc:ServiceException):
    return make_response({
        "success":False,
        "code":exc.code,
        "data":exc.data
    })

app.include_router(
    files_router,
    prefix="/file"
)

app.include_router(
    auth_router,
    prefix="/auth"
)
