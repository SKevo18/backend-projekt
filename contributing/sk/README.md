# Dokumentácia na vysvetlenie toho, čo som robil v kóde

V súbore `authentication.py` máme triedu `UserModel`, ktorá vyzerá takto:

```python
class UserModel(BaseModel): # model pre používateľa
    first_name: str
    last_name: str
    user_email: str
    user_password: str
    role: int
```

Táto trieda slúži na registráciu používateľa a určuje, aké údaje sa ukladajú do databázy. V súbore `orm.py` máme definovanú triedu `User`, ktorá vyzerá takto:

```python
class User(Base): __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    user_email: Mapped[str] = mapped_column(String(length=40), nullable=False, index=True)
    user_password: Mapped[str] = mapped_column(String(length=80), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
```

Tento kód ukazuje, ako sa údaje ukladajú na server a aké atribúty majú akú veľkosť. Napríklad `first_name` je typu `Mapped[str]`, čo znamená, že bude uložený ako reťazec s maximálnou dĺžkou 15 znakov. Ak bude hodnota dlhšia ako 15 znakov, uloží sa len prvých 15 a zvyšok sa vynechá. Toto platí aj pre `last_name`, `user_email` a `user_password`.

## Hasovanie hesla

Na hasovanie hesiel som použil knižnicu `passlib`. Funkcia na hasovanie hesla vyzerá takto:

```python
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

## Registrácia

V súbore `authentication.py` máme funkciu na registráciu používateľa:

```python
def register(user: UserModel, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter_by(user_email=user.user_email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = hash_password(user.user_password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        user_email=user.user_email,
        user_password=hashed_password,
        role=user.role,
        registered_at=datetime.now()
    )

    db.add(new_user)
    db.commit()

    token = create_access_token({"sub": new_user.user_email})
    return {"access_token": token, "token_type": "bearer"}
```

Tento kód overuje, či používateľ s daným e-mailom už existuje. Ak áno, vráti chybu, že používateľ už existuje. Ak nie, heslo je najprv zahashované, potom sa používateľ uloží do databázy. Následne sa vygeneruje prístupový token, ktorý sa vracia používateľovi.

## Prihlásenie

Prihlásenie funguje podobne ako registrácia, ale s rozdielom, že overujeme, či používateľ existuje a či sa heslo zhoduje s tým, čo je v databáze. Ak je heslo správne, vytvorí sa token. Rovnako ako pri registrácii, ak používateľ neexistuje alebo je heslo nesprávne, vráti sa chyba. Pre bezpečnosť nie je dobré písať konkrétne, čo je nesprávne (či e-mail alebo heslo).

## Token Access

Na vytváranie tokenov som použil knižnicu `pyjwt`. Tajný kľúč sa obvykle uchováva v `env` súbore, aby bol zabezpečený. Funkcia na vytváranie tokenov vyzerá takto:

```python
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=12)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta 
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

Funkcia na overenie tokenu je nasledovná:

```python
def verify_access_token(token: str):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) 
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

Token sa zvyčajne ukladá do `localStorage` na strane klienta. Tento spôsob nie je úplne bezpečný, ale budem sa tým zaoberať a študovať ďalšie možnosti ochrany.

## Frontend a Backend

Frontend komunikuje s backendom cez knižnicu `Axios`. Ak po prečítaní môjho kódu a dokumentácie máte nejaké nejasnosti, neváhajte sa opýtať. Pri najbližšom stretnutí sa môžeme dohodnúť na ďalšom vysvetlení a odpovedaní na otázky.

## Užitočné odkazy

1. [FastAPI](https://github.com/sebastiansKychatyi/sj_cvicenia_1/edit/main/README.md)
2. [Hash hesla](https://passlib.readthedocs.io/en/stable/)
3. [JWT](https://pyjwt.readthedocs.io/en/stable/)
4. [To, čo som pozrel ohľadom autentifikácie](https://www.youtube.com/watch?v=Ws-J7HbQ4nY&list=PLlKID9PnOE5jiWTTsshCXdz5qvg8JWezX&index=5&ab_channel=luchanos)
5. [OAuth2](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/)
6. [Autentifikácia vs autorizácia](https://habr.com/ru/articles/720842/)
7. [Viac informácií o JWT](https://habr.com/ru/articles/842056/)

Tieto odkazy sú zdroje, ktoré som používal. Rád by som, aby si ich aspoň raz pozrel, pretože teória je veľmi dôležitá. Niektoré odkazy sú v ruštine, ale ak je to problém, môžeš použiť Google Translate.
