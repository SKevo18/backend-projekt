import fastapi as fa

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test():
    return {"hello": "world"}


ALL_ROUTERS = [ROOT_ROUTER]
