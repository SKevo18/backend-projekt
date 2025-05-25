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
    - Windows: `.\.venv\Scripts\activate.ps1`
4. Inštalovať potrebné Python moduly cez PyPI: `pip install -r requirements.txt`
5. Pridať `DATABASE_URL` do env premenných (v súbore `.env`).
6. Spustiť uvicorn server: `uvicorn main:API --reload --env-file .env`
7. Nezabudajte na XAMPP
8. Neviem ci je to tak iba u mna ale ak sa nedari zapnut SQL v XAMPP tak treba otvorit "Task manager" -> mysql -> end task -> spustit XAMPP
9. tak isto moze sa vam stat z uvicorn preto cez "task manager" -> python -> end task -> sputit zas

## Production (Namecheap shared hosting)

1. [Kúpiť Namecheap shared hosting](https://www.namecheap.com/hosting/purchase/domain-connection/?product=stellar&addons=server-location%3Bserver-location-eu&duration=1&durationtype=month&domainType=NAMECHEAP)
2. Zmeniť nameservery existujúcej domény na tie od Namecheapu
3. Pripojiť sa do FTP (napr. Firezilla), viď [dokumentácia Namecheap](https://www.namecheap.com/support/knowledgebase/article.aspx/188/205/how-to-access-an-account-via-ftp/#ftp)
4. Upraviť `frontend/.env` súbor pre produkčné nastavenia, build cez `npm run build`
5. Upload obsahu priečinka `frontend/dist` do FTP (do `~/public_html/`), spolu s `.htaccess` pre reverse proxy na backend
6. Povoliť SSH pripojenie v Namecheap cPaneli
7. Vyhľadať "Terminal" v cPaneli, potom v home adresári (`~/`) dať `git clone https://github.com/SKevo18/backend-projekt app` (naklonovať repozitár do `~/app`, alebo do ľubovoľného iného adresára)
8. Vytvoriť databázu v cPaneli, potom podľa toho upraviť engine URL v `backend/.env`
9. Vyhľadať "Setup Python App" v cPaneli
10. "Create application":
    - Python version: 3.13
    - Application root: `/app/backend` (alebo adresár kde je `backend` priečinok v repozitári)
    - Application URL: nezáleží, toto vytvárame iba preto aby sme mali Python venv s inštalovanými packages a možnosť spustiť `run.py` cez cPanel
    - Application startup file: prepisuje existujúce súbory, zvoliť nejaký súbor čo sa môže vytvoriť a nikdy nepoužiť, napr. `abc.py`
    - Application entry point: teoreticky `API`, ale toto je nepodstatné, pretože `run.py` sa postará o spustenie API serveru
    - Environment variables: nepodstatné, pretože sú načítavané automaticky pri štarte aplikácie cez `python-dotenv` (stačí meniť `backend/.env`, skopírovať šablónu z `backend/.env.template` a zmeniť podľa potreby)
11. "Create"
12. Ak sa vytvorila, ideme na stránku tej Python aplikácie a v sekcii "Configuration files":
    - "requirements.txt" -> tlačidlo "Add"
    - "Run Pip install" > "requirements.txt"
    - počkať keď sa nainštalujú packages
13. V časi "Execute python script" spustiť `migrate.py`, aby sa vytvorili tabuľky v databáze a prebehli migrácie
14. Ďalej spustiť skript `run.py`, to spustí API server v pozadí (cez "Execute python script")
15. Teraz by malo byť možné ísť na adresu stránky a prihlásiť sa cez `admin@nieco.sk` a heslo `12345678` (po nastavení serveru ho treba zmeniť!)

## Užitočné odkazy

- [Swagger dokumentácia (keď beží API server)](http://localhost:8000/docs)
- [FastAPI dokumentácia](https://fastapi.tiangolo.com/)
- [SQLAlchemy tutoriál](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Uvicorn dokumentácia](https://www.uvicorn.org/)
- [Python docstrings](https://www.python.org/dev/peps/pep-0257/)
