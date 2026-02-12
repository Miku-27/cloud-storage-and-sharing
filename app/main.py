from fastapi import FastAPI
from app.api.file_route import files_route
from app.utils.exceptions import ServiceException
from app.utils.response import make_response

app = FastAPI()

@app.exception_handler(ServiceException)
async def handle_service_exception(exc:ServiceException):
    make_response({
        "success":False,
        "code":exc.code,
        "data":exc.data
    })

app.include_router(
    files_route,
    prefix="/file"
)
