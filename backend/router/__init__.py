import fastapi as fa

from router.page_crud import PAGE_CRUD_ROUTER

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test():
    return {"hello": "world"}


ALL_ROUTERS = [ROOT_ROUTER, PAGE_CRUD_ROUTER]
