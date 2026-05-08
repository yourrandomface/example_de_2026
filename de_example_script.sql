--товары
CREATE TABLE products (
    article TEXT PRIMARY KEY,               
    name TEXT NOT NULL,                        
    unit TEXT NOT NULL,                          
    price REAL NOT NULL,       
    supplier TEXT,                              
    manufacturer TEXT,                           
    category TEXT,                              
    discount REAL,
    stock_quantity INTEGER , 
    description TEXT,                            
    photo_url TEXT                            
);

-- пункты выдачи
CREATE TABLE pickup_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL UNIQUE              
);

-- пользователи
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,                        
    full_name TEXT NOT NULL,                   
    login TEXT NOT NULL UNIQUE,              
    password TEXT NOT NULL              
);

-- заказы
CREATE TABLE orders (
    order_number INTEGER PRIMARY KEY AUTOINCREMENT, 
    order_date DATE NOT NULL,  
    delivery_date DATE,                               
    pickup_point_id INTEGER NOT NULL,                 
    customer_full_name TEXT NOT NULL,                 
    pickup_code TEXT UNIQUE,                         
    order_status TEXT NOT NULL,       
    FOREIGN KEY (pickup_point_id) REFERENCES pickup_points(id)
);

-- товары в заказе
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number INTEGER NOT NULL,                  
    product_article TEXT NOT NULL,                  
    quantity INTEGER NOT NULL,
    FOREIGN KEY (order_number) REFERENCES orders(order_number),
    FOREIGN KEY (product_article) REFERENCES products(article)
);