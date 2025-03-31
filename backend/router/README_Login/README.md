# Login a Register – Jednoduchý systém autentifikácie

jednoduchý systém registrácie a prihlásenia, ktorý komunikuje so serverom cez JSON.

## Ako to funguje?
1. **Registrácia** a **Prihlásenie** fungujú cez odosielanie JSON súborov na server.
2. **Dáta sa ukladajú na serveri** – musí byť zapnutý, napríklad pomocou **XAMPP**.
3. **Heslá sú hashované**, čo znamená, že nie sú uložené v čitateľnej forme. Ak ich niekto dokáže dešifrovať, ponúkam **10$ odmenu** (aj keď si nie som istý, či je to vôbec možné).
4. **Hashovanie hesiel** – stále konzultujeme s **Kevinom**, pretože úplne nechápem, ako presne hash funguje.

## Dôležité informácie
- Odkazy na dokumentáciu sú **dole** – oplatí sa ich prečítať!

## Užitočné odkazy (Dokumentácia)
1. [SQLAlchemy – Funkcie (.commit, .user, atď.)](https://docs.sqlalchemy.org/en/20/core/functions.html)
2. [Passlib – Ako funguje hashovanie hesiel](https://passlib.readthedocs.io/en/stable/lib/passlib.context.html)
3. [Reddit – Ako funguje hashovanie hesiel a ako sa používa?](https://www.reddit.com/r/learnprogramming/comments/rov0to/how_does_password_hashing_workhow_is_it_used_in/?rdt=35315)
