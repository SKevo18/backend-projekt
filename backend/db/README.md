# Databáza

Modul s databázou (presnejšie: ORM modelmi) a [migráciami (cez Alembic)](./migrations/README.md).

## Dokumentácia

ORM modely definujeme **deklaratívnym mapovaním atribútov na stĺpce v databáze** (pozri ["Declarative Mapping" dokumentáciu](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html#declarative-mapping)). **Imperatívne mapovanie nepoužívame** (je zastaralé a v modernom SQLAlchemy sa neodporúča).

Tento dokument nebude ďalej popisovať ako definovať jednotlivé ORM modely, pretože tento proces je detailne obsiahnutý v dokumentácii SQLAlchemy. Prípade to poriešime formou diskusie v pull requestoch alebo issues na GitHube.
