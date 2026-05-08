import sqlite3


DB_PATH = "test"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def auth_user(login, password):
    with get_conn() as conn:
        cur = conn.execute(
            "SELECT id, role, full_name FROM users WHERE login=? AND password=?",
            (login, password)
        )
        return cur.fetchone()

def get_products(search="", supplier="", sort_stock=""):
    with get_conn() as conn:
        sql = "SELECT * FROM products WHERE 1=1"
        params = []
        if search:
            sql += " AND (name LIKE ? OR article LIKE ? OR description LIKE ? OR category LIKE ?)"
            params += [f"%{search}%"] * 4
        if supplier and supplier != "Все поставщики":
            sql += " AND supplier = ?"
            params.append(supplier)
        if sort_stock == "asc":
            sql += " ORDER BY stock_quantity ASC"
        elif sort_stock == "desc":
            sql += " ORDER BY stock_quantity DESC"
        else:
            sql += " ORDER BY name"
        return [dict(row) for row in conn.execute(sql, params).fetchall()]

def get_suppliers():
    with get_conn() as conn:
        return [r[0] for r in conn.execute("SELECT DISTINCT supplier FROM products WHERE supplier IS NOT NULL")]

def add_product(data):
    try:
        with get_conn() as conn:
            conn.execute("""
                INSERT INTO products (article,name,unit,price,supplier,manufacturer,category,discount,stock_quantity,description,photo_url)
                VALUES (?,?,?,?,?,?,?,?,?,?,?)
            """, tuple(data[k] for k in ["article","name","unit","price","supplier","manufacturer","category","discount","stock_quantity","description","photo_url"]))
            conn.commit()
            return True, ""
    except sqlite3.IntegrityError:
        return False, "Товар с таким артикулом уже существует"

def update_product(article, data):
    with get_conn() as conn:
        conn.execute("""
            UPDATE products SET name=?,unit=?,price=?,supplier=?,manufacturer=?,category=?,discount=?,stock_quantity=?,description=?,photo_url=?
            WHERE article=?
        """, tuple(data[k] for k in ["name","unit","price","supplier","manufacturer","category","discount","stock_quantity","description","photo_url"]) + (article,))
        conn.commit()
        return True

def delete_product(article):
    with get_conn() as conn:
        if conn.execute("SELECT 1 FROM order_items WHERE product_article=? LIMIT 1", (article,)).fetchone():
            return False, "Товар есть в заказах — удаление запрещено"
        photo = conn.execute("SELECT photo_url FROM products WHERE article=?", (article,)).fetchone()
        conn.execute("DELETE FROM products WHERE article=?", (article,))
        conn.commit()
        return True, ""

def in_orders(article):
    with get_conn() as conn:
        return conn.execute("SELECT 1 FROM order_items WHERE product_article=? LIMIT 1", (article,)).fetchone() is not None