<h3> Dokumentácia na vysvetlenie toho, čo som robil v kóde </h3>
<p> V súbore `authentication.py` máme triedu `UserModel`, ktorá vyzerá takto: 
</p> 
<pre> class UserModel(BaseModel): # model pre používateľa 
    first_name: str 
    last_name: str 
    user_email: str 
    user_password: str 
    role: int 
</pre> 
<p> Táto trieda slúži na registráciu používateľa a určuje, aké údaje sa ukladajú do databázy. V súbore `orm.py` máme definovanú triedu `User`, ktorá vyzerá takto: </p> <pre> 
    class User(Base): __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    last_name: Mapped[str] = mapped_column(String(length=15), nullable=False, index=True)
    user_email: Mapped[str] = mapped_column(String(length=40), nullable=False, index=True)
    user_password: Mapped[str] = mapped_column(String(length=80), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
</pre> 
<p> Tento kód ukazuje, ako sa údaje ukladajú na server a aké atribúty majú akú veľkosť. Napríklad `first_name` je typu `Mapped[str]`, čo znamená, že bude uložený ako reťazec s maximálnou dĺžkou 15 znakov. Ak bude hodnota dlhšia ako 15 znakov, uloží sa len prvých 15 a zvyšok sa vynechá. Toto platí aj pre `last_name`, `user_email` a `user_password`.</p> 
<h2> Hasovanie hesla </h2> 
<p> Na hasovanie hesiel som použil knižnicu `passlib`. Funkcia na hasovanie hesla vyzerá takto: </p> 
<pre> 
    def hash_password(password: str) -> str: 
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool: 
return pwd_context.verify(plain_password, hashed_password) 
</pre>

<h2> Registrácia </h2> 
<p> V súbore `authentication.py` máme funkciu na registráciu používateľa: </p> 
<pre> 
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

</pre> 
<p> Tento kód overuje, či používateľ s daným e-mailom už existuje. Ak áno, vráti chybu, že používateľ už existuje. Ak nie, heslo je najprv zahashované, potom sa používateľ uloží do databázy. Následne sa vygeneruje prístupový token, ktorý sa vracia používateľovi. </p> 
<h2> Prihlásenie </h2> 
<p> Prihlásenie funguje podobne ako registrácia, ale s rozdielom, že overujeme, či používateľ existuje a či sa heslo zhoduje s tým, čo je v databáze. Ak je heslo správne, vytvorí sa token. Rovnako ako pri registrácii, ak používateľ neexistuje alebo je heslo nesprávne, vráti sa chyba. Pre bezpečnosť nie je dobré písať konkrétne, čo je nesprávne (či e-mail alebo heslo). </p> 
<h2> Token Access </h2> 
<p> Na vytváranie tokenov som použil knižnicu `pyjwt`. Tajný kľúč sa obvykle uchováva v `env` súbore, aby bol zabezpečený. Funkcia na vytváranie tokenov vyzerá takto: </p> 
<pre> def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=12)): 
            to_encode = data.copy() 
            expire = datetime.now(timezone.utc) + expires_delta to_encode.update({"exp": expire}) encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256") 
            return encoded_jwt 
</pre>
<p> Funkcia na overenie tokenu je nasledovná: </p> 
<pre> def verify_access_token(token: str): 
    try: payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]) r
    eturn payload 
    except jwt.ExpiredSignatureError: 
    raise HTTPException(status_code=401, detail="Token expired") 
    except jwt.InvalidTokenError: 
    raise HTTPException(status_code=401, detail="Invalid token") 
</pre> 
<p> Token sa zvyčajne ukladá do `localStorage` na strane klienta. Tento spôsob nie je úplne bezpečný, ale budem sa tým zaoberať a študovať ďalšie možnosti ochrany. </p> 
<h2> Frontend a Backend </h2> 
<p> Frontend komunikuje s backendom cez knižnicu `Axios`. Ak po prečítaní môjho kódu a dokumentácie máte nejaké nejasnosti, neváhajte sa opýtať. Pri najbližšom stretnutí sa môžeme dohodnúť na ďalšom vysvetlení a odpovedaní na otázky. </p> 
<h2> Užitočné odkazy </h2> 
<p> 1. [FastAPI] <a href="https://github.com/sebastiansKychatyi/sj_cvicenia_1/edit/main/README.md">https://github.com/sebastiansKychatyi/sj_cvicenia_1/edit/main/README.md</a> 
</p> 
<p> 2. [Hash hesla] <a href="https://passlib.readthedocs.io/en/stable/">https://passlib.readthedocs.io/en/stable/</a> 
</p> 
<p> 3. [JWT] <a href="https://pyjwt.readthedocs.io/en/stable/">https://pyjwt.readthedocs.io/en/stable/</a> 
</p> 
<p> 4. [To, čo som pozrel ohľadom autentifikácie] <a href="https://www.youtube.com/watch?v=Ws-J7HbQ4nY&list=PLlKID9PnOE5jiWTTsshCXdz5qvg8JWezX&index=5&ab_channel=luchanos">https://www.youtube.com/watch?v=Ws-J7HbQ4nY&list=PLlKID9PnOE5jiWTTsshCXdz5qvg8JWezX&index=5&ab_channel=luchanos</a> 
</p> 
<p> 5. [OAuth2] <a href="https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/">https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/</a> 
</p>
<p> 6. [Autentifikácia vs autorizácia] <a href="https://habr.com/ru/articles/720842/">https://habr.com/ru/articles/720842/</a> 
</p> 
<p> 7. [Viac informácií o JWT] <a href="https://habr.com/ru/articles/842056/">https://habr.com/ru/articles/842056/</a> 
</p> 
<p> Tieto odkazy sú zdroje, ktoré som používal. Rád by som, aby si ich aspoň raz pozrel, pretože teória je veľmi dôležitá. Niektoré odkazy sú v ruštine, ale ak je to problém, môžeš použiť Google Translate. Ak máš akékoľvek otázky, pokojne sa opýtaj! :) </p>
