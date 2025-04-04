import fastapi as fa

from router.authentication import AUTH_ROUTER
from router.category_crud import CATEGORY_ROUTER
from router.email import EMAIL_ROUTER
from router.page_crud import PAGE_CRUD_ROUTER
from router.upload_controller import UPLOAD_CONTROLLER

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test():
    return {"hello": "world"}


ALL_CONTROLLERS = [
    ROOT_ROUTER,
    AUTH_ROUTER,
    CATEGORY_ROUTER,
    EMAIL_ROUTER,
    PAGE_CRUD_ROUTER,
    UPLOAD_CONTROLLER,
]
