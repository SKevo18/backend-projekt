# Docker Compose konfigurácia

Obsahuje Docker Compose konfiguráciu pre backend a frontend.

## Súbory

- [`Dockerfile` pre backend](../backend/Dockerfile)
- [`Dockerfile` pre frontend](../frontend/Dockerfile)
- [`docker-compose.yaml`](./docker-compose.yaml) pre definovanie služieb (ako má medzi sebou frontend a backend spolupracovať)
- Predvolený profil pre HTTP a profil `https` pre HTTPS podporu (s Certbotom pre SSL a Nginx HTTPS konfiguráciou)
  - HTTPS prostredie nebolo zatiaľ testované – je to zatiaľ iba teoretická konfigurácia

## Spustenie

- Mac/Linux: pozri [`dev.sh`](./dev.sh)
- Windows: pozri [`dev.ps1`](./dev.ps1)

Predtým, ako sa spustia príkazy vyššie, je potrebné aby bežal Docker Desktop. XAMPP a podobné záležitosti nie sú potrebné (Docker nemá nič s XAMPPom).

Po spustení skriptov je potrebné zadať heslo pre root používateľa MariaDB a aj heslo pre DB usera. Lokálne je to úplne jedno, na produkčnom serveri sa ale bude používať nejaké jednotné heslo (ak by došlo k takémuto scenáru).

## Princíp fungovania

Služby fungujú pod princípom SoC (Separation of Concerns = každá služba "si robí svoje" a nezasahuje do ostatných služieb):

- `backend`: FastAPI (cez `uvicorn`)
- `db`: MariaDB
- `frontend`: Frontend aplikácia s Nginx (predvolene, bez HTTPS)
- `frontend-https`: Frontend aplikácia s Nginx s HTTPS podporou (iba ak `--profile https`, netestované)
- `certbot`: Certbot pre správu SSL certifikátov (iba ak `--profile https`, netestované)

Všetky služby majú svoje vlastné izolované prostredie – a teda majú aj vlastný filesystem (ktorý môžu zdieľať cez "volume") a aj svoj vlastný network – Docker DNS manažuje rezolúciu hostov (napr. ak chceme Nginx poslať na uvicorn – resp. `backend` službu – použijeme `backend:8000`, čo znamená že sa odkazujeme na `localhost` v backendovej službe).

## Odkazy a zdroje

- [Docker Compose príklady](https://github.com/docker/awesome-compose)
- [Docker dokumentácia](https://docs.docker.com/get-started/)
- [Docker Compose dokumentácia](https://docs.docker.com/compose/gettingstarted/)
- [Nginx core dokumentácia](https://nginx.org/en/docs/ngx_core_module.html)
