# I. Dokumentácia pre CRUD systém: Kategórie a Stránky

Tento dokument detailne vysvetľuje, ako funguje systém kategórií a stránok v tomto projekte — od backendovej vrstvy (FastAPI, SQLAlchemy), cez stavovú vrstvu frontend aplikácie (Pinia), až po Vue komponenty, ktoré používateľ vidí a používa.

ORM → CRUD → Store → Komponenty → UX.
---

## 1. Backend architektúra (FastAPI + SQLAlchemy)

### 1.1 ORM modely (`orm.py`)

#### Category model:

```python
class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(45), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    pages: Mapped[list["Page"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )
```

- Uchováva kategórie ako „roky“ alebo „sekcie“.
- Vzťah `pages` umožňuje načítať všetky stránky v rámci kategórie.
- `cascade="all, delete-orphan"` zabezpečuje zmazanie všetkých stránok, ak sa odstráni kategória.

#### Page model:

```python
class Page(Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    html_content: Mapped[t.Text] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    edited_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, nullable=True)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    category: Mapped["Category"] = relationship(back_populates="pages")
```

- Reprezentuje obsahovú stránku, ktorá patrí do určitej kategórie.
- `edited_at` sa aktualizuje pri zmene obsahu.
- `category` definuje vzťah medzi modelom `Page` a `Category` pomocou `relationship()`. Je to obojstranný (bidirectional) vzťah, ktorý umožňuje prístup ku kategórii danej stránky (`page.category`) aj ku všetkým stránkam kategórie (`category.pages`).

---

## 2. CRUD operácie

### 2.1 `category_crud.py`

```python
CATEGORY_ROUTER = APIRouter(prefix="/category")
```

- `POST /category/` — pridanie novej kategórie
- `GET /category/` — získanie zoznamu kategórií

Príklad:

```json
POST /category/
{ "title": "2025" }

GET /category/
→ [
  { "id": 1, "title": "2025", "created_at": "..." },
  ...
]
```

---

### 2.2 `page_crud.py`

```python
PAGE_CRUD_ROUTER = APIRouter(prefix="/page")
```

- `POST /page/` — vytvorenie stránky
- `GET /page/{id}` — získanie detailu
- `GET /page/` — zoznam všetkých stránok
- `PUT /page/{id}` — úprava stránky
- `DELETE /page/{id}` — odstránenie stránky

Príklad:

```json
POST /page/
{
  "title": "Úvod",
  "html_content": "<p>Vitajte!</p>",
  "category_id": 1
}
```

---

## 3. Frontend architektúra (Vue + Pinia)

### 3.1 Pinia Store — `pageStore.ts`

```ts
export const usePagesStore = defineStore("pages", { ... });
```

**Stav:**
- `pages: Page[]` — všetky stránky
- `categories: Category[]` — všetky kategórie
- `error: string | null` — stav chyby

**Akcie:**
- `fetchPages()` — GET /page/
- `fetchCategories()` — GET /category/
- `addPage(...)` — POST /page/
- `addCategory(...)` — POST /category/
- `updatePage(...)` — PUT /page/{id}
- `deletePage(...)` — DELETE /page/{id}

```ts
await api.post('/page/', newPage);
```

---

## 4. Vue komponenty

### 4.1 `AdminPagesView.vue` — hlavný admin panel

Funkcie:
- Pridávanie stránok ku kategóriám
- Pridávanie nových kategórií
- Aktualizácia a zmazanie stránok
- Formuláre reagujú dynamicky podľa kategórie

```ts
await this.pagesStore.addPage(category.id, this.title, this.html_content);
```

- Využíva computed properties `sortedPages` a `sortedCategories`
- Pri načítaní komponentu volá `fetchPages()` a `fetchCategories()`

---

### 4.2 `HeaderComponent.vue` — hlavička a navigácia

- Dynamicky zobrazuje:
  - Linky na login/register (ak je používateľ neprihlásený)
  - Linky na administráciu a logout (ak je prihlásený)
- Vytvára navigáciu podľa kategórií

```ts
<RouterLink v-for="category in sortedCategories" :to="`/${category.title}`">
  {{ category.title }}
</RouterLink>
```

---

## 5. Komunikácia frontend ↔ backend

### Štruktúra komunikácie:

| Frontend akcia           | HTTP request        | Backend endpoint     | Výsledok                    |
|--------------------------|---------------------|-----------------------|-----------------------------|
| Pridať stránku           | `POST /page/`       | `create_page()`       | Nová stránka v DB           |
| Získať všetky stránky    | `GET /page/`        | `read_all_pages()`    | Zoznam stránok              |
| Upraviť stránku          | `PUT /page/{id}`    | `update_page()`       | Úprava záznamu              |
| Zmazať stránku           | `DELETE /page/{id}` | `delete_page()`       | Odstránenie stránky         |
| Získať kategórie         | `GET /category/`    | `list_categories()`   | Zoznam kategórií            |
| Pridať kategóriu         | `POST /category/`   | `create_category()`   | Nová kategória v databáze   |

**Príklad z `pageStore.ts`:**

```ts
const response = await api.post('/page/', {
  title: "O projekte",
  html_content: "<p>Informácie...</p>",
  category_id: 1
});
this.pages.push(response.data);
```

---

## 6. Validácia a UX

- Základná validácia pomocou `try-catch` blokov pri sieťových požiadavkách.
- Alerty pre používateľa pri duplikátoch názvu kategórie alebo stránky.
- Chybové hlášky sa ukladajú do `this.error` pre zobrazenie vo UI.

### Príklady:

#### Duplikát názvu kategórie:
```ts
if (!this.categories.some(cat => cat.title === title)) {
    // POST request
} else {
    alert(`Kategória "${title}" už existuje.`);
}
```

#### Duplikát názvu stránky:
```ts
if (!this.pages.some(page => page.title === title)) {
    // POST request
} else {
    alert(`Stránka s názvom "${title}" už existuje.`);
}
```

#### Chytanie chýb (napr. pri načítaní stránok):
```ts
try {
    const response = await api.get('/page/');
    this.pages = response.data;
} catch (error) {
    this.error = 'Nepodarilo sa načítať stránky.';
}
```

---

## Záver

Celý systém predstavuje prepojený CRUD ekosystém, kde:

- SQLAlchemy definuje dátové modely  
- FastAPI poskytuje REST API  
- Pinia spravuje frontendový stav  
- Vue komponenty tvoria vizuálne rozhranie
