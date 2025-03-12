# Migrácie

Migračné skripty pre definovanie zmien v databáze sú spravované pomocou Python modulu [Alembic](https://alembic.sqlalchemy.org/en/latest/), ktorý je navrhnutý pre nami používaný ORM modul [SQLAlchemy](https://www.sqlalchemy.org/).

Zdrojový kód pre migrácie sa nachádza v priečinku [`migrations`](./). Fungujú nezávisle od ORM schémy, ktorá je definovaná pre najnovšiu (aktuálnu) verziu aplikácie v súbore [`db/orm.py`](../orm.py).

Zmysel migrácií je popísať, ako sa databáza mení naprieč verziami aplikácie a automatizovať vykonávanie týchto zmien – toto ORM schéma nedokáže, pretože je iba abstrakciou nad databázou a nemá v sebe samotnú funkcionalitu pre migrácie. Preto je potrebné použiť externý nástroj, akým je v našom prípade Alembic (ak by sa to malo *veľmi zjednodušiť*, tak migrácie sú vlastne ako nejaký "git pre databázu").

## Správa migrácií

Všetky migrácie sa spravujú pomocou terminálu cez príkaz `alembic`, ktorý je platformovo nezávislý a funguje rovnako ako na Macu a Linuxe, tak aj na Windowse (ak je tento modul správne nainštalovaný vo venv a to venv je aktivované). S každým príkazom `alembic` sa musíme nachádzať v priečinku pre migrácie, to jest:

```bash
cd backend/db/migrations # ak predpokladáme, že aktuálne sme v koreňovom adresári projektu
```

### Pridanie novej migrácie

Stručy postup:

1. Zmeniť ORM schému v [`db/orm.py`](../orm.py) (pridať model, vymazať atribút a podobne...);
2. Vytvoriť novú migráciu (`alembic revision --autogenerate -m "popis_migracie"`);
3. Upraviť migráciu v priečinku [`versions`](./versions) (ak je to potrebné – vo väčšine prípadov by nemalo);
4. Aplikovať migráciu do databázy (`alembic upgrade head`);

Najčastejšie budeme používať tento príkaz. Robíme to zakaždým, keď zmeníme ORM schému databázy v súbore [`db/orm.py`](../orm.py):

```bash
alembic revision --autogenerate -m "popis_migracie"
```

Funguje to tak, že Alembic porovná aktuálnu ORM schému oproti aktuálnemu stavu databázy a vygeneruje novú migráciu automaticky, ktorá bude obsahovať všetky zmeny oproti minulej verzii databázy. Následne sa v priečinku [`versions`](./versions) objaví nový súbor s definovanou migráciou (je možné ho upravovať, ak sa migrácia v niektorých prípadoch vygeneruje zle). Do správy (`-m`) vkladáme stručný popis toho, čo migrácia robí, v angličtine (napríklad: `create_user_table`, `seed_admin`, `add_role_column`, a podobne).

Alternatívne je možné vygenerovať prázdnu migráciu (teda, bez flagu `--autogenerate`):

```bash
alembic revision -m "popis_migracie"
```

V tom prípade je potrebné manuálne definovať funkcie `upgrade` a `downgrade` v generovanom súbore.

#### `FAILED: Target database is not up to date.` chyba

Je potrebné databázu upgradovať na najnovšiu verziu, prostredníctvom `alembic upgrade head` (pozri nižšie).

### Aplikovanie migrácií

Robí sa to pomocou podpríkazu `upgrade`. Ako argument sa posiela ID revízie, ktorú chceme aplikovať. V našom prípade je to `head`, čo znamená, že budú aplikované všetky novšie migrácie.

```bash
alembic upgrade head
```

Je dôležité, že pokiaľ vytvoríme nejakú migráciu a spustíme ju, už ju nemeníme! Ak sme urobili nejakú chybu počas lokálneho vývoja a aj tak chceme zmeniť migráciu (napríklad, ešte sme neodoslali pull request), môžeme to spraviť pokial urobíme downgrade a následne znovu aplikujeme tú istú (opravenú) migráciu (pozri nižšie).

### Vrátenie ("odstránenie") poslednej migrácie

Ak sme sa napríklad pomýlili ale schéma samotnej databázy je už zmenená, znamená to že musíme vrátiť databázu do predošlého stavu, respektíve odstrániť poslednú aplikovanú migráciu. Robí sa to pomocou nasledovného príkazu (ako flag sa posiela číslo = o koľko migrácií sa má vrátiť, v našom prípade `-1` znamená vrátiť sa o jednu migráciu nazad, teda revertovať poslednú aplikovanú migráciu):

```bash
alembic downgrade -1
```

Samozrejme sa predpokladá, že je v migráciách správne definovaná funkcia `downgrade`. Ak nie, tak príkaz zlyhá.

### Zoznam všetkých migrácií

Ak chceme zobraziť všetky migrácie a ich stav, použijeme podpríkaz `history`:

```bash
alembic history
```

### Vytvorenie seedu

Migrácie v Alembicu môžeme použiť aj pre vloženie predvolených dát do databázy (seedov). Pozri napríklad súbor [`versions/56fa62a328fa_seed_admin.py`](./versions/56fa62a328fa_seed_admin.py), ktorý vytvára admina.

Seedy používame pre definovanie základných dát v databáze bez ktorých aplikácia nemôže fungovať (napríklad, aplikácia musí mať údaje o administrátorovi a nejaké základné odkazy a nastavenia). Seedy sú minimalistické, a nepoužívame ich pre definovanie dát ktoré bude pridávať samotný používateľ (napríklad konkrétne účty používateľov alebo stránky, a podobne)!

## Užitočné odkazy

- [Alembic dokumentácia](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
