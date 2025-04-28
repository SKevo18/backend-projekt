import fastapi as fa

from controllers.authentication_controller import AUTH_CONTROLLER
from controllers.category_controller import CATEGORY_CONTROLLER
from controllers.email_controller import EMAIL_CONTROLLER
from controllers.page_controller import PAGE_CONTROLLER
from backend.controllers.permission_controller import PERMISSION_CONTROLLER
from controllers.settings_controller import SETTINGS_CONTROLLER
from controllers.upload_controller import UPLOAD_CONTROLLER
from controllers.user_controller import USER_CONTROLLER

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test():
    return {"hello": "world"}


ALL_CONTROLLERS = [
    ROOT_ROUTER,
    AUTH_CONTROLLER,
    CATEGORY_CONTROLLER,
    EMAIL_CONTROLLER,
    PAGE_CONTROLLER,
    PERMISSION_CONTROLLER,
    SETTINGS_CONTROLLER,
    UPLOAD_CONTROLLER,
    USER_CONTROLLER,
]
