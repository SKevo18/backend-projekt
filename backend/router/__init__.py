import fastapi as fa

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test():
    return {"Sebp": "world"}

@ROOT_ROUTER.get("/")
def test1():
    return {"sebo": "Kzchatzi"}

@ROOT_ROUTER.get("/")
def test2():
    return {"sasha": "uzdzumaki"}

ALL_ROUTERS = [ROOT_ROUTER]
