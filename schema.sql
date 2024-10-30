-- Roles Table
CREATE TABLE Roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    role_id INTEGER REFERENCES Roles(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Categories Table
CREATE TABLE Categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(255),
    parent_id INTEGER REFERENCES Categories(id) ON DELETE SET NULL,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Products Table
CREATE TABLE Products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(255),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    category_id INTEGER REFERENCES Categories(id) ON DELETE RESTRICT ON UPDATE CASCADE,
    image_path VARCHAR(255),  -- Путь к файлу
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Order_statuses Table
CREATE TABLE Order_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Orders Table
CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(id) ON DELETE CASCADE,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_price DECIMAL(10, 2),
    status_id INTEGER REFERENCES Order_statuses(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Order_items Table
CREATE TABLE Order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES Orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES Products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL,
    price_at_purchase DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Индексы
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_products_name ON Products(name);
CREATE INDEX idx_products_category_id ON Products(category_id);
CREATE INDEX idx_orders_user_id ON Orders(user_id);
CREATE INDEX idx_orders_status_id ON Orders(status_id);

-- Выдать ПРАВА админу
GRANT USAGE ON SCHEMA public TO shop_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO shop_admin;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO shop_admin;



-- DATA
INSERT INTO Roles (name) VALUES ('user'), ('admin');


INSERT INTO Categories (name, description, created_at, updated_at)
VALUES
('Collection X', 'Описание для Collection X', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Collection Z', 'Описание для Collection Z', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Collection V', 'Описание для Collection V', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);



INSERT INTO Products (name, description, price, stock_quantity, is_active, category_id, image_path, created_at, updated_at)
VALUES
('Ёлочная игрушка 1', 'Описание игрушки 1', 500.0, 10, TRUE, 1, '/static/images/1.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ёлочная игрушка 2', 'Описание игрушки 2', 300.0, 15, TRUE, 1, '/static/images/2.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ёлочная игрушка 3', 'Описание игрушки 3', 800.0, 20, TRUE, 1, '/static/images/3.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ёлочная игрушка 4', 'Описание игрушки 4', 600.0, 5, TRUE, 2, '/static/images/4.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ёлочная игрушка 5', 'Описание игрушки 5', 400.0, 7, TRUE, 2, '/static/images/5.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('Ёлочная игрушка 6', 'Описание игрушки 6', 500.0, 15, TRUE, 3, '/static/images/6.png', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);


-- Статусы заказов
новый
в обработке
отправлен
получен
завершен
отменен
возвращен
--
