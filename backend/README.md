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

---

## Docker (Odporúčané)

Najjednoduchší spôsob ako spustiť celú aplikáciu (backend + frontend + databáza).

### Požiadavky

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) alebo Docker Engine (Linux)

### Rýchly štart

1. **Spustite Docker Desktop** (musí bežať pred spustením príkazov)

2. **Prejdite do docker priečinka:**
   ```bash
   cd docker
   ```

3. **Vytvorte `.env` súbor** (skopírujte šablónu):
   ```bash
   # Linux/Mac:
   cp .env.example .env

   # Windows (PowerShell):
   Copy-Item .env.example .env
   ```

4. **Upravte `.env` súbor** - nastavte heslá:
   ```env
   DB_ROOT_PASSWORD=moje_root_heslo
   DB_PASSWORD=moje_app_heslo
   SECRET_KEY=nahodny_tajny_kluc
   ```

5. **Spustite aplikáciu:**
   ```bash
   # Linux/Mac:
   ./dev.sh

   # Windows (PowerShell):
   .\dev.ps1
   ```

   Alebo manuálne:
   ```bash
   docker compose --profile default up --build -d
   ```

6. **Aplikácia beží na:**
   - Frontend: http://localhost
   - API dokumentácia: http://localhost/api/docs
   - Databáza: localhost:3306

### Užitočné príkazy

```bash
# Zobraziť logy
docker compose logs -f

# Zobraziť logy konkrétnej služby
docker compose logs -f backend

# Zastaviť aplikáciu
docker compose down

# Zastaviť a vymazať dáta (databáza)
docker compose down -v

# Reštartovať službu
docker compose restart backend

# Vstúpiť do kontajnera
docker compose exec backend bash
docker compose exec db mysql -u app -p app
```

### Štruktúra služieb

| Služba | Port | Popis |
|--------|------|-------|
| `frontend` | 80 | Vue.js + Nginx |
| `backend` | 8000 (interný) | FastAPI + Uvicorn |
| `db` | 3306 | MariaDB 11 |

### Riešenie problémov

**Port 80 je obsadený:**
```bash
# Windows - nájsť proces:
netstat -ano | findstr :80

# Zastaviť IIS ak beží:
iisreset /stop
```

**Databáza sa nespustí:**
```bash
# Vymazať volumes a spustiť znova:
docker compose down -v
docker compose --profile default up --build -d
```

**Backend padá:**
```bash
# Skontrolovať logy:
docker compose logs backend
```

---

## Development inštrukcie (bez Dockera)

Ak nechcete používať Docker, môžete spustiť backend manuálne s XAMPP.

### Požiadavky

- Python 3.13+
- XAMPP (alebo iný MySQL/MariaDB server)

### Kroky

1. **Prejdite do backend priečinka:**
   ```bash
   cd backend
   ```

2. **Vytvorte virtual environment:**
   ```bash
   python -m venv .venv
   ```

3. **Aktivujte virtual environment:**
   ```bash
   # Mac/Linux:
   source .venv/bin/activate

   # Windows (PowerShell):
   .\.venv\Scripts\activate.ps1

   # Windows (CMD):
   .\.venv\Scripts\activate.bat
   ```

4. **Nainštalujte závislosti:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Vytvorte `.env` súbor** (skopírujte šablónu):
   ```bash
   cp .env.template .env
   ```

6. **Upravte `.env` súbor:**
   ```env
   DATABASE_URL=mysql+pymysql://root@localhost:3306/bp
   SECRET_KEY=nahodny_tajny_kluc
   FRONTEND_URL=http://localhost:5173
   ```

7. **Spustite XAMPP** a vytvorte databázu `bp` v phpMyAdmin

8. **Spustite migrácie:**
   ```bash
   python migrate.py
   ```

9. **Spustite server:**
   ```bash
   uvicorn main:API --reload --env-file .env
   ```

10. **API beží na:** http://localhost:8000/docs

### Časté problémy

- **MySQL v XAMPP sa nespustí:** Otvorte Task Manager -> nájdite `mysql` -> End task -> spustite XAMPP znova
- **Uvicorn nereaguje:** Task Manager -> nájdite `python` -> End task -> spustite znova

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
12. Ak sa vytvorila, tú stránku **vypneme** (tlačidlo stop, s plným štvorcom) a ideme na stránku tej Python aplikácie a v sekcii "Configuration files":
    - "requirements.txt" -> tlačidlo "Add"
    - "Run Pip install" > "requirements.txt"
    - počkať keď sa nainštalujú packages
13. V časi "Execute python script" spustiť `migrate.py`, aby sa vytvorili tabuľky v databáze a prebehli migrácie
14. Ďalej spustiť skript `run.py`, to spustí API server v pozadí (cez "Execute python script")
15. Teraz by malo byť možné ísť na adresu stránky a prihlásiť sa cez `admin@nieco.sk` a heslo `12345678` (po nastavení serveru ho treba zmeniť!)

### Aktualizovanie aplikácie

1. Ísť do terminálu, `cd app` a `git pull` pre stiahnutie najnovších zmien z repozitára
    - ak nastali nejaké zmeny v `backend/` priečinku a boli zahrnuté vo version control a neboli commitnuté, tak to bude problém
    - ak nemáme čas a chceme jednoducho iba najnovšiu synchronizovanú verziu a zahodniť existujúce zmeny ktoré sme vykonali cez FTP, tak jednoducho vymažeme `~/app/backend/` priečinok cez FTP a znovu ho naklonujeme cez `git clone https://github.com/SKevo18/backend-projekt app`
2. Spustiť `migrate.py` cez "Execute python script" v cPaneli, pre zmeny DB schémy
3. Spustiť `run.py` cez "Execute python script" v cPaneli, aby sa spustil API server s najnovšími zmenami

### Automatický reštart

Predvolene, Namecheap kill-ne procesy ktoré sú nečinné. Dá sa to vyriešiť vytvorením cronjobu ktorý bude bežať každých 5 minút a bude reštartovať API server, stačí iba spustiť `run.py`:

```cron
*/5 * * * * /usr/bin/python3 /home/dbbaoird/app/backend/run.py --cron
```

## Užitočné odkazy

- [Swagger dokumentácia (keď beží API server)](http://localhost:8000/docs)
- [FastAPI dokumentácia](https://fastapi.tiangolo.com/)
- [SQLAlchemy tutoriál](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- [Uvicorn dokumentácia](https://www.uvicorn.org/)
- [Python docstrings](https://www.python.org/dev/peps/pep-0257/)
