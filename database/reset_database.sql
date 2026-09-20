-- PrePlate Database Schema - Restaurant Management System
-- This script will completely recreate the database with the new schema

-- Drop existing database and recreate
DROP DATABASE IF EXISTS preplate_db;
CREATE DATABASE preplate_db;
USE preplate_db;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'reception', 'kitchen') NOT NULL DEFAULT 'reception',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food items table with stock and preparation time
CREATE TABLE food_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT DEFAULT 0,
    preparation_time INT DEFAULT 0,
    image VARCHAR(255),
    available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Orders table for restaurant workflow
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    table_number VARCHAR(20),
    subtotal DECIMAL(10, 2) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    estimated_preparation_time INT DEFAULT 0,
    status ENUM('Pending', 'Preparing', 'Ready', 'Completed', 'Cancelled') DEFAULT 'Pending',
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Order items table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (food_id) REFERENCES food_items(id) ON DELETE RESTRICT
);

-- Daily sales table for tracking
CREATE TABLE daily_sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sale_date DATE NOT NULL UNIQUE,
    total_orders INT DEFAULT 0,
    completed_orders INT DEFAULT 0,
    total_revenue DECIMAL(10, 2) DEFAULT 0.00,
    items_sold INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert default admin user
-- Password: Admin@123 (will be hashed on first login)
INSERT INTO users (name, email, password, role) VALUES
('Restaurant Admin', 'admin@preplate.com', 'placeholder_hash', 'admin');

-- Insert sample reception staff
INSERT INTO users (name, email, password, role) VALUES
('Reception Staff', 'reception@preplate.com', 'placeholder_hash', 'reception');

-- Insert sample kitchen staff
INSERT INTO users (name, email, password, role) VALUES
('Kitchen Staff', 'kitchen@preplate.com', 'placeholder_hash', 'kitchen');

-- Insert sample categories
INSERT INTO categories (name) VALUES
('Pizza'),
('Burger'),
('Indian'),
('Chinese'),
('Desserts'),
('Beverages'),
('Snacks'),
('Pasta');

-- Insert sample food items with stock and preparation time
INSERT INTO food_items (category_id, name, description, price, stock_quantity, preparation_time, image, available) VALUES
(1, 'Margherita Pizza', 'Fresh mozzarella, tomato sauce and basil', 249.00, 15, 15, 'pizza_margherita.jpg', TRUE),
(1, 'Pepperoni Pizza', 'Classic pepperoni with cheese and tomato sauce', 299.00, 12, 15, 'pizza_pepperoni.jpg', TRUE),
(1, 'Veggie Supreme', 'Bell peppers, onions, mushrooms and olives', 279.00, 10, 15, 'pizza_veggie.jpg', TRUE),
(2, 'Cheese Burger', 'Juicy beef patty with melted cheese and fresh vegetables', 179.00, 25, 10, 'burger_cheese.jpg', TRUE),
(2, 'Chicken Burger', 'Crispy chicken fillet with special sauce', 199.00, 20, 12, 'burger_chicken.jpg', TRUE),
(2, 'Veggie Burger', 'Plant-based patty with avocado and lettuce', 169.00, 18, 8, 'burger_veggie.jpg', TRUE),
(3, 'Veg Biryani', 'Aromatic basmati rice with mixed vegetables and spices', 189.00, 30, 20, 'biryani_veg.jpg', TRUE),
(3, 'Paneer Tikka', 'Marinated paneer grilled with spices', 229.00, 15, 15, 'paneer_tikka.jpg', TRUE),
(3, 'Butter Chicken', 'Tender chicken in rich tomato butter gravy', 259.00, 20, 25, 'butter_chicken.jpg', TRUE),
(4, 'Veg Fried Rice', 'Stir-fried rice with mixed vegetables', 149.00, 35, 10, 'fried_rice_veg.jpg', TRUE),
(4, 'Chicken Manchurian', 'Spicy chicken balls in Indo-Chinese sauce', 219.00, 18, 15, 'manchurian_chicken.jpg', TRUE),
(4, 'Hakka Noodles', 'Stir-fried noodles with vegetables', 159.00, 30, 12, 'noodles_hakka.jpg', TRUE),
(5, 'Chocolate Brownie', 'Rich chocolate brownie with vanilla ice cream', 129.00, 20, 5, 'brownie_chocolate.jpg', TRUE),
(5, 'Cheesecake', 'Creamy New York style cheesecake', 149.00, 15, 5, 'cheesecake.jpg', TRUE),
(5, 'Gulab Jamun', 'Traditional Indian sweet dumplings in sugar syrup', 99.00, 25, 5, 'gulab_jamun.jpg', TRUE),
(6, 'Cold Coffee', 'Chilled coffee with ice cream', 89.00, 20, 5, 'coffee_cold.jpg', TRUE),
(6, 'Mango Smoothie', 'Fresh mango blended with yogurt', 109.00, 15, 5, 'smoothie_mango.jpg', TRUE),
(6, 'Fresh Lime Soda', 'Refreshing lime soda with mint', 59.00, 50, 3, 'lime_soda.jpg', TRUE),
(7, 'French Fries', 'Crispy golden fries with seasoning', 79.00, 40, 8, 'fries.jpg', TRUE),
(7, 'Onion Rings', 'Crispy battered onion rings', 89.00, 25, 8, 'onion_rings.jpg', TRUE),
(7, 'Garlic Bread', 'Toasted bread with garlic butter and herbs', 69.00, 30, 5, 'garlic_bread.jpg', TRUE),
(8, 'Pasta Alfredo', 'Creamy white sauce pasta with vegetables', 189.00, 20, 15, 'pasta_alfredo.jpg', TRUE),
(8, 'Pasta Arrabbiata', 'Spicy tomato sauce pasta', 179.00, 18, 15, 'pasta_arrabbiata.jpg', TRUE),
(8, 'Mac and Cheese', 'Classic macaroni with cheese sauce', 169.00, 22, 12, 'mac_cheese.jpg', TRUE);
