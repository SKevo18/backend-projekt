# Backend

Zdrojový kód pre FastAPI aplikáciu.

## Štruktúra

- `main.py` - hlavný súbor, ktorý spúšťa FastAPI aplikáciu a berie routery z `router/__init__.py` (`ALL_ROUTERS`)
- `router` - modul s routermi
  - ak sa vytvorí nový router, importuje sa do `router/__init__.py` a zahrnie sa do `ALL_ROUTERS`
- `db` - modul s databázou a ORM modelmi
  - `__init__.py` - inicializácia databázy, pripojenia a ORM modelov
  - `orm.py` - súbor s ORM modelmi

## Development inštrukcie

1. `cd backend`
2. `python -m venv .venv`
3. Aktivovať virtual environment:
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `.\.venv\Scripts\activate`
4. `pip install -r requirements.txt`
5. Pridať `DATABASE_URL` do env premenných, napr.:
    - Mac/Linux: `export DATABASE_URL="sqlite:///db.sqlite"`
    - Windows: `set DATABASE_URL="sqlite:///db.sqlite"`
6. `uvicorn main:API --reload`
    - alebo: `python main.py`

## Užitočné odkazy

- [Swagger dokumentácia (keď beží API server)](http://localhost:8000/docs)
- [FastAPI dokumentácia](https://fastapi.tiangolo.com/)
- [SQLAlchemy tutoriál](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Uvicorn dokumentácia](https://www.uvicorn.org/)
- [Python docstrings](https://www.python.org/dev/peps/pep-0257/)
