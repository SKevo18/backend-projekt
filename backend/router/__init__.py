import fastapi as fa
from sqlalchemy import select

from db import DB
import db.orm as orm

ROOT_ROUTER = fa.APIRouter()


@ROOT_ROUTER.get("/")
def test(test_id: int):
    test = DB.session.scalars(select(orm.Test).filter(orm.Test.id == test_id)).first()
    if test is None:
        raise fa.HTTPException(status_code=404, detail=f"test {test_id} not found")

    return {"id": test.id, "data": test.data}


@ROOT_ROUTER.post("/")
def create_test(data: str):
    test = orm.Test(data=data)
    DB.session.add(test)
    DB.session.commit()

    return {"data": test.id}


ALL_ROUTERS = [ROOT_ROUTER]
