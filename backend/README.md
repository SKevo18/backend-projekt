# Backend

Zdrojový kód pre FastAPI aplikáciu.

## Štruktúra

- `README.md` - tento súbor
- `main.py` - hlavný súbor, ktorý spúšťa FastAPI aplikáciu a berie routery z `router/__init__.py` (`ALL_ROUTERS`)
- `requirements.txt` - súbor s potrebnými Python modulmi (cez PyPI)
- `router/` - modul s routermi
  - `README.md` - dokumentácia k routerom
  - `__init__.py` - inicializácia routerov (ak sa vytvorí nový router, zahrnie sa do `ALL_ROUTERS` v tomto súbore)
- `db/` - modul s databázou a ORM modelmi
  - `__init__.py` - inicializácia databázy, pripojenia a ORM modelov
  - `orm.py` - súbor s ORM modelmi ("databázovou schémou")
  - `migrations/` - priečinok s migráciami
    - `README.md` - dokumentácia k migráciám
    - `env.py` - súbor s konfiguráciou pre Alembic
    - `versions/` - priečinok s vygenerovanými migráciami

## Development inštrukcie

1. `cd backend`
2. `python -m venv .venv`
3. Aktivovať virtual environment:
    - Mac/Linux: `source .venv/bin/activate`
    - Windows: `.\.venv\Scripts\activate`
4. Inštalovať potrebné Python moduly cez PyPI: `pip install -r requirements.txt`
5. Pridať `DATABASE_URL` do env premenných (v súbore `.env`). Následne exportovať premenné. V prípade [Windowsu](https://stackoverflow.com/a/72236585/23509205):

    ```powershell
    get-content .env | foreach {
      $name, $value = $_.split('=')
      set-content env:\$name $value
    }
    ```

    V prípade Macu/Linuxu:

    ```bash
    export $(cat .env | xargs)
    ```

    (alebo prostredníctvom `direnv allow` a `.envrc` súboru namiesto `.env` (viď [direnv dokumentácia](https://direnv.net/)))

6. Spustiť uvicorn server: `uvicorn main:API --reload`
    - alebo: `python main.py`

## Užitočné odkazy

- [Swagger dokumentácia (keď beží API server)](http://localhost:8000/docs)
- [FastAPI dokumentácia](https://fastapi.tiangolo.com/)
- [SQLAlchemy tutoriál](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Uvicorn dokumentácia](https://www.uvicorn.org/)
- [Python docstrings](https://www.python.org/dev/peps/pep-0257/)
