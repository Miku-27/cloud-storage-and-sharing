from fastapi import APIRouter,Depends
from app.models.database import get_db
from app.dependencies import validate_jwt
from app.models.schemas import FileFilters
from app.utils.response import make_response
from app.services.file_service import get_user_file_service
from sqlalchemy.orm import Session

user_router = APIRouter()

@user_router.get("/me/files")
def get_user_file_route(filters:FileFilters = Depends(),db:Session=Depends(get_db),user_id:int=Depends(validate_jwt)):
    response = get_user_file_service(db,user_id,filters.model_dump(exclude_none=True))
    return make_response(response)
