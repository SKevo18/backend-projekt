# Projekt – Backendové technológie (FPVaI UKF 2025)

Tímový projekt pre predmet "Backendové technológie" (FPVaI UKF 2025) v 4. semestri bakalárskeho štúdia. Repozitár slúži pre obhajobu riešenia, pre zdieľanie a spoluprácu na zdrojovom kóde a pre definovanie postupov pri vývoji.

## Plán

### Ako to bude vyzerať

- **Frontend**: Vue 3;
- **Backend**: FastAPI (čisté REST API) + SQLAlchemy (ORM);
- **Docker**: Nginx + PHP-FPM;

### Úlohy

- Definovať základnú Docker konfiguráciu - potrebujeme kontajner pre Nginx + Uvicorn (alebo iný vhodný Python webserver), PHP-FPM, MariaDB...
- Definovať databázovú štruktúru (aké sú entity a atribúty - budeme používať [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/quickstart.html))
- Definovať databázové migrácie - pravdepodobne [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
  - Definovať seedy pre databázu (tiež cez Alembic)
- Autentifikácia a autorizácia:
  - Login stránka (frontend)
  - Registrácia (frontend)
  - Spojenie s backednom cez REST API
    - Access token sa uloží v databáze a na strane klienta ako cookie s atribútom `HttpOnly` (kvôli [bezpečnosti](https://securinglaravel.com/security-tip-what-is-an-httponly-cookie/)). Token sa potom používa automaticky pri každom requeste cez cookie (`fetch({credentials: 'same-origin'})`, čo je predvolene nastavené pre [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch))
- Admin panel:
  - Pridanie ďalších admin používateľov (CRUD)
    - Úvaha: **iba hlavný admin bude môcť pridávať iných adminov**, alebo **akýkoľvek admin vie pridať ďalších adminov**?
  - CRUD (frontend + backend):
  - WYSIWYG editor musí mať validáciu, proti JS injekcii, atď. (napríklad: na backend sa odošle HTML, ktoré sa vyčistí - cez [nh3](https://nh3.readthedocs.io/en/latest/))
- Používateľské zobrazenie
  - Registrácia + login
  - Registračný e-mail (cez SMTP a Gmail, ako proof-of-concept)
  - atď...

### Potenciálne vylepšenia

- Určite Let's Encrypt certifikáty cez certbot, pre HTTPS (aktualizovať Nginx konfiguráciu)
- Riešiť všetko cez pull requesty a issues (tak, ako sa to má normálne robiť)?
- Dať konečné riešenie na vlastný server a nejakú doménu, ako proof-of-concept?
- Cloudflare (proti DDoS, atď.)?
- Postfix ako e-mailový server (pravdepodobne overkill, môžeme použiť Gmail, aj tak je to iba prototyp)?
- [chroot](https://nrdmnn.net/resources/3-Secure-webspaces-with-NGINX-PHP-FPM-chroots-and-Lets-Encrypt)? Je v tom benefit, keď to bude v Dockeri?

### Užitočné odkazy

- [Zabezpečenie Nginx + PHP-FPM cez chroot + Let's Encrypt](https://nrdmnn.net/resources/3-Secure-webspaces-with-NGINX-PHP-FPM-chroots-and-Lets-Encrypt)
- [Zoznam WYSIWYG editorov pre Vue 3](https://github.com/JefMari/awesome-wysiwyg-editors?tab=readme-ov-file#for-vue)
- [Vue 3 dokumentácia](https://vuejs.org/guide/introduction.html)
- [Alembic dokumentácia](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [SQLAlchemy dokumentácia](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [FastAPI dokumentácia](https://fastapi.tiangolo.com/tutorial/)
- [Nginx dokumentácia](https://nginx.org/en/docs/)
- [PHP-FPM dokumentácia](https://www.php.net/manual/en/install.fpm.php)
- [Docker dokumentácia](https://docs.docker.com/)
- [Cloudflare dokumentácia](https://developers.cloudflare.com/fundamentals/get-started/reference/network-ports/)
