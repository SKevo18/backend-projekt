# Projekt – Backendové technológie (FPVaI UKF 2025)

Tímový projekt pre predmet "Backendové technológie" (FPVaI UKF 2025) v 4. semestri bakalárskeho štúdia. Repozitár slúži pre obhajobu riešenia, pre zdieľanie a spoluprácu na zdrojovom kóde a pre definovanie postupov pri vývoji.

## Stručný popis projektu

Účelom projektu je vytvorenie funkčného prototypu konferenčného reakčného systému. Aplikácia musí byť schopná zvládnuť 2 úrovne prístupu:

1. Anonymný - používateľ, ktorý dokáže prezerať obsah prístupný pre verejnosť
2. Administrátor - používateľ schopný vkladať obsah

Uvedený softvér spadá do kategórie [Content Management System (CMS)](https://wikipedia.org/wiki/Content_management_system) so špecifickým zameraním. Preto je potrebné, aby uvedený systém spĺňal všetky náležitosti ktoré sú pre tento typ systému charakteristické, akými sú spravovanie používateľov s administračným prístupom alebo základné úpravy vizuálu, atď...

### Základné funkčné požiadavky

- Aplikácia musí obsahovať prihlasovanie/registráciu administrátorov;
- Administrátor musí vedieť vykonávať CRUD operácie pre stage;
- Administrátor musí vedieť vykonávať CRUD operácie pre časové okná v existujúcich stagoch;
- Administrátor musí vedieť vykonávať CRUD operácie pre profily speakerov - obrázok/krátky popis/dlhý popis/linky na sociálne siete;
- Administrátor musí vedieť vykonávať CRUD operácie pre prednášky k jednotlivým speakerom - krátky popis/dlhý popis;
- Administrátor musí vedieť prideľovať prednášky do jednotlivých časových slotov;
- Administrátor musí vedieť vytvoriť sponzora;
- Administrátor musí mať možnosť vytvorenia galérie - kategorické rozdelenie na ročníky;
- Používateľ sa musí vedieť zaregistrovať na konferenciu;
- Po registrácii je potrebné aby prišiel registračný email na predvolenú adresu ako aj na adresu používateľa;
- Používateľ sa musí vedieť odhlásiť z konferencie;
- Administrátor musí vedieť kto sa na danú konferenciu zaregistroval;
- Používateľ pri prihlasovaní sa na konferenciu musí mať možnosť výberu s jednotlivých prednášok - validácia časových okien (nedovoliť vybrať 2 prednášky v tom istom čase);
- Administrátor musí mať možnosť nastavovať kapacitu jednotlivých prednášok - toto sa musí prejavovať aj pri registrácii;
- Administrátor musí vedieť vykonávať CRUD operácie nad sekciou "Povedali o nás" - foto, výrok;
- Administrátor musí vedieť za pomoci WYSIWYG editora vytvárať vlastné stránky - príklad: "Ochrana osobných údajov";
- Všetky obsahové sekcie ktoré administrátor vie vytvoriť musia byť prístupné pre používateľov;

## Plán

### Ako to bude vyzerať

1. Pri prvom spustení aplikácie bude výzva pre nastavenie administrátora (email, heslo) a pripojenia k databáze (podobne ako WordPress)
2. Bude základné blokové rozloženie hlavnej stránky, odkazy v header a footer
3. Databáza sa naseeduje s predvolenými hodnotami, admin ich môže meniť cez CRUD: stage, speaker, atď...

- **Frontend**: Vue 3;
- **Backend**: FastAPI (čisté REST API) + SQLAlchemy (ORM);
- **Docker**: Nginx + PHP-FPM;

**Príklad:** [https://nconnect.sk](https://nconnect.sk)

### Úlohy

- Definovať základnú Docker konfiguráciu - potrebujeme kontajner pre Nginx, PHP-FPM, MariaDB
- Definovať databázovú štruktúru (aké sú entity a atribúty - budeme používať [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/quickstart.html))
- Spraviť setup screen (Vue)
  - Uloženie údajov pre pripojenie k databáze v JSON súbore (backend)
  - Pripojenie k databáze (backend)
- Definovať databázové migrácie - pravdepodobne [Alembic]([https://alembic.sqlalchemy.org/en/latest/](https://alembic.sqlalchemy.org/en/latest/tutorial.html))
  - Definovane seedov pre databázu (basically skript, ktorý naplní databázu predvolenými hodnotami, aby bolo čo editovať a aby stránka nebola prázdna ale nejako vyzerala)
- Autentifikácia a autorizácia:
  - Login stránka (frontend)
  - Registrácia (frontend)
  - Spojenie s backednom cez REST API
    - Access token sa uloží v databáze a na strane klienta ako cookie s atribútom `HttpOnly` (kvôli [bezpečnosti](https://securinglaravel.com/security-tip-what-is-an-httponly-cookie/)). Token sa potom používa automaticky pri každom requeste cez cookie (`fetch({credentials: 'same-origin'})`, čo je predvolene nastavené pre [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch))
- Admin panel:
  - Pridanie ďalších admin používateľov (CRUD)
    - Úvaha: **iba hlavný admin bude môcť pridávať iných adminov**, alebo **akýkoľvek admin vie pridať ďalších adminov**?
  - CRUD (frontend + backend):
    - Stage
    - Speaker
    - Prednášky (aj s kapacitou, t. j. nemôže sa prihlásiť viac ľudí ako je povolená kapacita prednášky)
      - Budeme riešiť aj "UKF situáciu" kedy sa všetci vrhnú na 1 termín naraz ako hladné supy za 5 sekúnd a backend nestíha a prihlási sa viac ľudí ako je povolená kapacita? T. j. ak sa presiahne kapacita, zoradíme podľa času prihlásenia a vyhodíme posledných `n` ľudí, aby to bolo v rámci kapacity
    - Časový harmonogram / časové sloty (ako som to ja pochopil, jedna prednáška môže mať viacero termínov v iný čas, a teda nemožno definovať dve prednášky v rovnaký čas)
    - Povedali o nás
    - Galéria (môže byť vlastný názov albumu, predvolene to bude aktuálny rok)
    - Sponzori (logo, názov, odkaz)
    - Kontakt, mapa (cez [Google Maps API](https://developers.google.com/maps/documentation/javascript/overview), [vue3-google-map package](https://www.npmjs.com/package/vue3-google-map))
    - Stránky ([WYSIWYG editor](https://github.com/JefMari/awesome-wysiwyg-editors?tab=readme-ov-file#for-vue), pravdepodobne [TinyMCE](https://github.com/tinymce/tinymce-vue) alebo [Quill](https://vueup.github.io/vue-quill/) – najlepšie taký, ktorý má priamo package s podporou pre Vue 3)
      - WYSIWYG editor musí mať validáciu, proti JS injekcii, atď. (na backend sa odošle HTML, ktoré sa vyčistí - cez [nh3](https://nh3.readthedocs.io/en/latest/))
      - Predvolene "Ochrana osobných údajov"
      - atď...?
- Používateľské zobrazenie
  - Registrácia + login
  - Registračný e-mail (cez SMTP a Gmail, ako proof-of-concept)
  - Prihlásenie na konferenciu (prednášku), odhlásenie z konferencie
  - Odhlásenie

### Potenciálne vylepšenia

- Určite Let's Encrypt certifikáty cez certbot, pre HTTPS (aktualizovať Nginx konfiguráciu)
- Riešiť všetko cez pull requesty a issues (tak, ako sa to má normálne robiť)?
- Dať konečné riešenie na vlastný server a nejakú doménu, ako proof-of-concept?
- Cloudflare (proti DDoS, atď.)?
- [chroot](https://nrdmnn.net/resources/3-Secure-webspaces-with-NGINX-PHP-FPM-chroots-and-Lets-Encrypt)?
- Postfix ako e-mailový server (pravdepodobne overkill, môžeme použiť Gmail, aj tak je to iba prototyp)?

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
