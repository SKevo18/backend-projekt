# FastAPI routery

Ak sa pridá nový router, musí byť zahrnutý v `ALL_ROUTERS` v súbore `main.py`.

Napr. vytvorím nový router `user_router.py` v premennej `USER_ROUTER` (pre CRUD operácie nad používateľmi).

```python
USER_ROUTER = APIRouter(
    prefix="/user",  # prefix, ktorý sa pridá pred všetky cesty v tomto routeri
)
```

...tak potom tento router musí byť pridaný do zoznamu `ALL_ROUTERS` v súbore `main.py`:

```python
from router.user_router import USER_ROUTER

ALL_ROUTERS = [
    USER_ROUTER,
]
```

Túto premennú `ALL_ROUTERS` potom berie `main.py` a pridáva ich do FastAPI aplikácie automaticky.

## Dokumentácia

- [FastAPI routery](https://fastapi.tiangolo.com/tutorial/bigger-applications/#apirouter)
