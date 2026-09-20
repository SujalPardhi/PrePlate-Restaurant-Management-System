from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from mysql.connector import Error, IntegrityError
from datetime import datetime, date, timedelta
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_NAME']
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Login required decorator
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Role required decorator
def role_required(*allowed_roles):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page.', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in allowed_roles:
                flash('You are not authorized to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# ==================== HOME PAGE ====================
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('public_dashboard'))

# ==================== PUBLIC DASHBOARD ====================
@app.route('/public')
def public_dashboard():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get active orders for public display (Pending, Preparing, Ready)
        # Only show 8 orders at a time, ordered by priority
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE o.status IN ('Pending', 'Preparing', 'Ready')
            ORDER BY 
                CASE o.status
                    WHEN 'Ready' THEN 1
                    WHEN 'Preparing' THEN 2
                    WHEN 'Pending' THEN 3
                END,
                o.created_at ASC
            LIMIT 8
        """)
        active_orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('public_dashboard.html', active_orders=active_orders)
    
    flash('Database connection error. Please try again later.', 'danger')
    return render_template('login.html')

# ==================== AUTHENTICATION ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter email and password.', 'warning')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                # Check if password is placeholder (first-time setup) - work for ALL accounts
                if user['password'] == 'placeholder_hash':
                    # Allow Admin@123 for all accounts as initial password
                    if password == 'Admin@123':
                        # Hash the password and update
                        hashed_password = generate_password_hash(password)
                        conn = get_db_connection()
                        if conn:
                            cursor = conn.cursor()
                            cursor.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password, email))
                            conn.commit()
                            cursor.close()
                            conn.close()
                        
                        # Set session and login
                        session['user_id'] = user['id']
                        session['user_name'] = user['name']
                        session['user_email'] = user['email']
                        session['role'] = user['role']
                        
                        flash(f'Welcome, {user["name"]}! Password has been secured.', 'success')
                        return redirect(url_for('dashboard'))
                    else:
                        flash('Invalid email or password.', 'danger')
                        return redirect(url_for('login'))
                
                # Normal password check
                if check_password_hash(user['password'], password):
                    session['user_id'] = user['id']
                    session['user_name'] = user['name']
                    session['user_email'] = user['email']
                    session['role'] = user['role']
                    
                    flash(f'Welcome, {user["name"]}!', 'success')
                    return redirect(url_for('dashboard'))
                else:
                    flash('Invalid email or password.', 'danger')
                    return redirect(url_for('login'))
            else:
                flash('Invalid email or password.', 'danger')
                return redirect(url_for('login'))
        
        flash('Database connection error. Please try again later.', 'danger')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ==================== DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        role = session.get('role')
        
        if role == 'admin':
            # Admin dashboard statistics
            today = date.today()
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(created_at) = %s", (today,))
            today_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Preparing'")
            preparing_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed' AND DATE(created_at) = %s", (today,))
            completed_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE DATE(created_at) = %s", (today,))
            today_sales = float(cursor.fetchone()['total'])
            
            cursor.execute("SELECT SUM(stock_quantity) as total FROM food_items")
            total_stock = cursor.fetchone()['total'] or 0
            
            # Recent orders
            cursor.execute("""
                SELECT o.*, 
                       (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
                FROM orders o 
                ORDER BY o.created_at DESC 
                LIMIT 10
            """)
            recent_orders = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return render_template('admin/dashboard.html', 
                                 today_orders=today_orders,
                                 pending_orders=pending_orders,
                                 preparing_orders=preparing_orders,
                                 ready_orders=ready_orders,
                                 completed_orders=completed_orders,
                                 today_sales=today_sales,
                                 total_stock=total_stock,
                                 recent_orders=recent_orders)
        
        elif role == 'reception':
            # Reception dashboard
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed' AND DATE(created_at) = CURDATE()")
            completed_today = cursor.fetchone()['count']
            
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE DATE(created_at) = CURDATE()")
            today_sales = float(cursor.fetchone()['total'])
            
            # Recent orders
            cursor.execute("""
                SELECT o.*, 
                       (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
                FROM orders o 
                ORDER BY o.created_at DESC 
                LIMIT 10
            """)
            recent_orders = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return render_template('reception/dashboard.html',
                                 pending_orders=pending_orders,
                                 ready_orders=ready_orders,
                                 completed_today=completed_today,
                                 today_sales=today_sales,
                                 recent_orders=recent_orders)
        
        elif role == 'kitchen':
            # Kitchen dashboard
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Preparing'")
            preparing_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            # Pending orders for kitchen
            cursor.execute("""
                SELECT o.*, 
                       (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
                FROM orders o 
                WHERE o.status IN ('Pending', 'Preparing')
                ORDER BY o.created_at ASC
            """)
            kitchen_orders = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            return render_template('kitchen/dashboard.html',
                                 pending_orders=pending_orders,
                                 preparing_orders=preparing_orders,
                                 ready_orders=ready_orders,
                                 kitchen_orders=kitchen_orders)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('login'))

# ==================== API ENDPOINTS FOR REAL-TIME UPDATES ====================
@app.route('/api/dashboard/stats')
@login_required
def dashboard_stats_api():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        role = session.get('role')
        
        if role == 'admin':
            today = date.today()
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(created_at) = %s", (today,))
            today_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Preparing'")
            preparing_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed' AND DATE(created_at) = %s", (today,))
            completed_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE DATE(created_at) = %s", (today,))
            today_sales = float(cursor.fetchone()['total'])
            
            cursor.execute("SELECT SUM(stock_quantity) as total FROM food_items")
            total_stock = cursor.fetchone()['total'] or 0
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'today_orders': today_orders,
                'pending_orders': pending_orders,
                'preparing_orders': preparing_orders,
                'ready_orders': ready_orders,
                'completed_orders': completed_orders,
                'today_sales': float(today_sales),
                'total_stock': int(total_stock) if total_stock else 0
            })
        
        elif role == 'reception':
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed' AND DATE(created_at) = CURDATE()")
            completed_today = cursor.fetchone()['count']
            
            cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE DATE(created_at) = CURDATE()")
            today_sales = float(cursor.fetchone()['total'])
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'pending_orders': pending_orders,
                'ready_orders': ready_orders,
                'completed_today': completed_today,
                'today_sales': float(today_sales)
            })
        
        elif role == 'kitchen':
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            pending_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Preparing'")
            preparing_orders = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Ready'")
            ready_orders = cursor.fetchone()['count']
            
            cursor.close()
            conn.close()
            
            return jsonify({
                'pending_orders': pending_orders,
                'preparing_orders': preparing_orders,
                'ready_orders': ready_orders
            })
    
    return jsonify({'error': 'Database connection error'}), 500

@app.route('/api/dashboard/recent-orders')
@login_required
def recent_orders_api():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            ORDER BY o.created_at DESC 
            LIMIT 10
        """)
        recent_orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({'recent_orders': recent_orders})
    
    return jsonify({'error': 'Database connection error'}), 500

# ==================== RECEPTION: CREATE ORDER ====================
@app.route('/reception/new-order', methods=['GET', 'POST'])
@role_required('reception', 'admin')
def new_order():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get all food items
        cursor.execute("""
            SELECT f.*, c.name as category_name 
            FROM food_items f 
            JOIN categories c ON f.category_id = c.id 
            WHERE f.available = TRUE AND f.stock_quantity > 0
            ORDER BY c.name, f.name
        """)
        food_items = cursor.fetchall()
        
        # Get categories
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('reception/new_order.html', food_items=food_items, categories=categories)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/reception/create-order', methods=['POST'])
@role_required('reception', 'admin')
def create_order():
    try:
        # Get order data
        customer_name = request.form.get('customer_name')
        table_number = request.form.get('table_number')
        items = request.form.getlist('items')
        quantities = request.form.getlist('quantities')
        
        # Validation
        if not customer_name:
            flash('Customer name is required.', 'warning')
            return redirect(url_for('new_order'))
        
        if not items or not quantities:
            flash('Please add at least one item to the order.', 'warning')
            return redirect(url_for('new_order'))
        
        # Process order items
        order_items_data = []
        subtotal = 0.0
        max_preparation_time = 0
        
        conn = get_db_connection()
        if not conn:
            flash('Database connection error.', 'danger')
            return redirect(url_for('new_order'))
        
        cursor = conn.cursor(dictionary=True)
        
        # Start transaction
        conn.start_transaction()
        
        try:
            for i, item_id in enumerate(items):
                quantity = int(quantities[i])
                if quantity <= 0:
                    continue
                
                # Get food item details
                cursor.execute("SELECT * FROM food_items WHERE id = %s", (item_id,))
                food = cursor.fetchone()
                
                if not food:
                    raise Exception(f"Food item {item_id} not found")
                
                # Check stock
                if food['stock_quantity'] < quantity:
                    raise Exception(f"Insufficient stock for {food['name']}. Available: {food['stock_quantity']}, Requested: {quantity}")
                
                # Calculate item total (convert Decimal to float)
                item_price = float(food['price'])
                item_total = item_price * quantity
                subtotal += item_total
                
                # Track preparation time
                if food['preparation_time'] > max_preparation_time:
                    max_preparation_time = food['preparation_time']
                
                order_items_data.append({
                    'food_id': item_id,
                    'quantity': quantity,
                    'price': item_price,
                    'subtotal': item_total
                })
            
            if not order_items_data:
                raise Exception("No valid items in order")
            
            # Create order
            cursor.execute("""
                INSERT INTO orders (customer_name, table_number, subtotal, total_amount, estimated_preparation_time, status, created_by)
                VALUES (%s, %s, %s, %s, %s, 'Pending', %s)
            """, (customer_name, table_number, subtotal, subtotal, max_preparation_time, session['user_id']))
            
            order_id = cursor.lastrowid
            
            # Add order items and update stock
            for item_data in order_items_data:
                # Add order item
                cursor.execute("""
                    INSERT INTO order_items (order_id, food_id, quantity, price, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (order_id, item_data['food_id'], item_data['quantity'], item_data['price'], item_data['subtotal']))
                
                # Update stock
                cursor.execute("""
                    UPDATE food_items 
                    SET stock_quantity = stock_quantity - %s 
                    WHERE id = %s
                """, (item_data['quantity'], item_data['food_id']))
            
            # Update daily sales
            today = date.today()
            total_items = sum(item['quantity'] for item in order_items_data)
            cursor.execute("""
                INSERT INTO daily_sales (sale_date, total_orders, items_sold, total_revenue)
                VALUES (%s, 1, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    total_orders = total_orders + 1,
                    items_sold = items_sold + %s,
                    total_revenue = total_revenue + %s
            """, (today, total_items, subtotal, total_items, subtotal))
            
            # Commit transaction
            conn.commit()
            
            cursor.close()
            conn.close()
            
            flash(f'Order #{order_id} created successfully!', 'success')
            return redirect(url_for('order_details', order_id=order_id))
            
        except Exception as e:
            # Rollback on error
            conn.rollback()
            cursor.close()
            conn.close()
            flash(f'Error creating order: {str(e)}', 'danger')
            return redirect(url_for('new_order'))
    
    except Exception as e:
        flash(f'Error processing order: {str(e)}', 'danger')
        return redirect(url_for('new_order'))

# ==================== ORDER DETAILS ====================
@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get order details
        cursor.execute("""
            SELECT o.*, u.name as created_by_name 
            FROM orders o 
            LEFT JOIN users u ON o.created_by = u.id 
            WHERE o.id = %s
        """, (order_id,))
        order = cursor.fetchone()
        
        if order:
            # Get order items
            cursor.execute("""
                SELECT oi.*, f.name as food_name, f.preparation_time 
                FROM order_items oi 
                JOIN food_items f ON oi.food_id = f.id 
                WHERE oi.order_id = %s
            """, (order_id,))
            order_items = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            role = session.get('role')
            if role == 'kitchen':
                return render_template('kitchen/order_details.html', order=order, order_items=order_items)
            elif role == 'reception':
                return render_template('reception/order_details.html', order=order, order_items=order_items)
            else:
                return render_template('admin/order_details.html', order=order, order_items=order_items)
        
        cursor.close()
        conn.close()
    
    flash('Order not found.', 'danger')
    return redirect(url_for('dashboard'))

# ==================== KITCHEN: UPDATE ORDER STATUS ====================
@app.route('/kitchen/update-status/<int:order_id>', methods=['POST'])
@role_required('kitchen', 'admin')
def update_order_status(order_id):
    new_status = request.form.get('status')
    
    valid_statuses = ['Pending', 'Preparing', 'Ready', 'Completed', 'Cancelled']
    
    if new_status not in valid_statuses:
        flash('Invalid status.', 'danger')
        return redirect(url_for('order_details', order_id=order_id))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (new_status, order_id))
        conn.commit()
        
        # Update daily sales if completed
        if new_status == 'Completed':
            cursor.execute("""
                UPDATE daily_sales 
                SET completed_orders = completed_orders + 1 
                WHERE sale_date = CURDATE()
            """)
            conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Order status updated successfully.', 'success')
        return redirect(url_for('order_details', order_id=order_id))
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('order_details', order_id=order_id))

# ==================== ADMIN: MENU MANAGEMENT ====================
@app.route('/admin/menu')
@role_required('admin')
def admin_menu():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT f.*, c.name as category_name 
            FROM food_items f 
            JOIN categories c ON f.category_id = c.id 
            ORDER BY c.name, f.name
        """)
        food_items = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/menu.html', food_items=food_items)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/admin/menu/add', methods=['GET', 'POST'])
@role_required('admin')
def add_food():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        stock_quantity = request.form.get('stock_quantity')
        preparation_time = request.form.get('preparation_time')
        image = request.form.get('image')
        available = request.form.get('available') == 'on'
        
        # Validation
        if not name or not price or not category_id:
            flash('Name, price, and category are required.', 'warning')
            return redirect(url_for('add_food'))
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be positive.', 'warning')
                return redirect(url_for('add_food'))
        except ValueError:
            flash('Invalid price.', 'warning')
            return redirect(url_for('add_food'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                INSERT INTO food_items (category_id, name, description, price, stock_quantity, preparation_time, image, available)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (category_id, name, description, price, stock_quantity or 0, preparation_time or 0, image, available))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Food item added successfully.', 'success')
            return redirect(url_for('admin_menu'))
        
        flash('Database connection error. Please try again later.', 'danger')
        return redirect(url_for('add_food'))
    
    # GET request - show form
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/add_food.html', categories=categories)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/edit/<int:food_id>', methods=['GET', 'POST'])
@role_required('admin')
def edit_food(food_id):
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        stock_quantity = request.form.get('stock_quantity')
        preparation_time = request.form.get('preparation_time')
        image = request.form.get('image')
        available = request.form.get('available') == 'on'
        
        # Validation
        if not name or not price or not category_id:
            flash('Name, price, and category are required.', 'warning')
            return redirect(url_for('edit_food', food_id=food_id))
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be positive.', 'warning')
                return redirect(url_for('edit_food', food_id=food_id))
        except ValueError:
            flash('Invalid price.', 'warning')
            return redirect(url_for('edit_food', food_id=food_id))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute("""
                UPDATE food_items 
                SET category_id = %s, name = %s, description = %s, price = %s, stock_quantity = %s, preparation_time = %s, image = %s, available = %s
                WHERE id = %s
            """, (category_id, name, description, price, stock_quantity, preparation_time, image, available, food_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            flash('Food item updated successfully.', 'success')
            return redirect(url_for('admin_menu'))
        
        flash('Database connection error. Please try again later.', 'danger')
        return redirect(url_for('edit_food', food_id=food_id))
    
    # GET request - show form
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM food_items WHERE id = %s", (food_id,))
        food = cursor.fetchone()
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        if food:
            return render_template('admin/edit_food.html', food=food, categories=categories)
        else:
            flash('Food item not found.', 'danger')
            return redirect(url_for('admin_menu'))
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('admin_menu'))

@app.route('/admin/menu/toggle/<int:food_id>')
@role_required('admin')
def toggle_food_availability(food_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT available FROM food_items WHERE id = %s", (food_id,))
        result = cursor.fetchone()
        
        if result:
            new_status = not result['available']
            cursor.execute("UPDATE food_items SET available = %s WHERE id = %s", (new_status, food_id))
            conn.commit()
            
            status_text = 'enabled' if new_status else 'disabled'
            flash(f'Food item {status_text}.', 'success')
        else:
            flash('Food item not found.', 'danger')
        
        cursor.close()
        conn.close()
    else:
        flash('Database connection error. Please try again later.', 'danger')
    
    return redirect(url_for('admin_menu'))

# ==================== ADMIN: ORDERS ====================
@app.route('/admin/orders')
@role_required('admin')
def admin_orders():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get filters
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        date_filter = request.args.get('date', '')
        
        # Build query
        query = """
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (o.id LIKE %s OR o.customer_name LIKE %s)"
            search_pattern = f'%{search}%'
            params.extend([search_pattern, search_pattern])
        
        if status:
            query += " AND o.status = %s"
            params.append(status)
        
        if date_filter:
            query += " AND DATE(o.created_at) = %s"
            params.append(date_filter)
        
        query += " ORDER BY o.created_at DESC"
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/orders.html', orders=orders, search=search, 
                             selected_status=status, selected_date=date_filter)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

# ==================== ADMIN: CATEGORIES ====================
@app.route('/admin/categories')
@role_required('admin')
def admin_categories():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM categories ORDER BY name")
        categories = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/categories.html', categories=categories)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/admin/categories/add', methods=['POST'])
@role_required('admin')
def add_category():
    name = request.form.get('name')
    
    if not name:
        flash('Category name is required.', 'warning')
        return redirect(url_for('admin_categories'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (name,))
            conn.commit()
            flash('Category added successfully.', 'success')
        except IntegrityError:
            flash('Category already exists.', 'warning')
        
        cursor.close()
        conn.close()
    else:
        flash('Database connection error. Please try again later.', 'danger')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/edit/<int:category_id>', methods=['POST'])
@role_required('admin')
def edit_category(category_id):
    name = request.form.get('name')
    
    if not name:
        flash('Category name is required.', 'warning')
        return redirect(url_for('admin_categories'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("UPDATE categories SET name = %s WHERE id = %s", (name, category_id))
            conn.commit()
            flash('Category updated successfully.', 'success')
        except IntegrityError:
            flash('Category name already exists.', 'warning')
        
        cursor.close()
        conn.close()
    else:
        flash('Database connection error. Please try again later.', 'danger')
    
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@role_required('admin')
def delete_category(category_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Check if category has food items
        cursor.execute("SELECT COUNT(*) as count FROM food_items WHERE category_id = %s", (category_id,))
        count = cursor.fetchone()['count']
        
        if count > 0:
            flash('Cannot delete category that contains food items.', 'warning')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_categories'))
        
        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Category deleted successfully.', 'success')
        return redirect(url_for('admin_categories'))
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('admin_categories'))

# ==================== ADMIN: STAFF MANAGEMENT ====================
@app.route('/admin/staff')
@role_required('admin')
def admin_staff():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users ORDER BY role, name")
        staff = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('admin/staff.html', staff=staff)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/admin/staff/add', methods=['POST'])
@role_required('admin')
def add_staff():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    role = request.form.get('role')
    
    # Validation
    if not name or not email or not password or not role:
        flash('All fields are required.', 'warning')
        return redirect(url_for('admin_staff'))
    
    if len(password) < 6:
        flash('Password must be at least 6 characters long.', 'warning')
        return redirect(url_for('admin_staff'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash('Email already registered.', 'warning')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_staff'))
        
        # Create new staff member
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
            (name, email, hashed_password, role)
        )
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Staff member added successfully.', 'success')
        return redirect(url_for('admin_staff'))
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('admin_staff'))

@app.route('/admin/staff/delete/<int:user_id>', methods=['POST'])
@role_required('admin')
def delete_staff(user_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Check if user is admin
        cursor.execute("SELECT role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        
        if user and user['role'] == 'admin':
            flash('Cannot delete admin users.', 'warning')
            cursor.close()
            conn.close()
            return redirect(url_for('admin_staff'))
        
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        flash('Staff member removed successfully.', 'success')
        return redirect(url_for('admin_staff'))
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('admin_staff'))

# ==================== ADMIN: REPORTS ====================
@app.route('/admin/reports')
@role_required('admin')
def admin_reports():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        today = date.today()
        
        # Today's statistics
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(created_at) = %s", (today,))
        today_orders = cursor.fetchone()['count']
        
        cursor.execute("SELECT COALESCE(SUM(total_amount), 0) as total FROM orders WHERE DATE(created_at) = %s", (today,))
        today_sales = float(cursor.fetchone()['total'])
        
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Completed' AND DATE(created_at) = %s", (today,))
        completed_today = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM orders WHERE status = 'Cancelled' AND DATE(created_at) = %s", (today,))
        cancelled_today = cursor.fetchone()['count']
        
        # Orders by status
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM orders 
            GROUP BY status
        """)
        orders_by_status = cursor.fetchall()
        
        # Most ordered food items
        cursor.execute("""
            SELECT f.name, SUM(oi.quantity) as total_quantity, SUM(oi.subtotal) as total_revenue
            FROM order_items oi
            JOIN food_items f ON oi.food_id = f.id
            GROUP BY f.id, f.name
            ORDER BY total_quantity DESC
            LIMIT 10
        """)
        popular_items = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for item in popular_items:
            item['total_revenue'] = float(item['total_revenue'])
        
        # Daily sales trend
        cursor.execute("""
            SELECT sale_date, total_orders, completed_orders, total_revenue, items_sold
            FROM daily_sales
            ORDER BY sale_date DESC
            LIMIT 30
        """)
        daily_sales = cursor.fetchall()
        
        # Convert Decimal to float for JSON serialization
        for day in daily_sales:
            day['total_revenue'] = float(day['total_revenue'])
        
        cursor.close()
        conn.close()
        
        return render_template('admin/reports.html',
                             today_orders=today_orders,
                             today_sales=today_sales,
                             completed_today=completed_today,
                             cancelled_today=cancelled_today,
                             orders_by_status=orders_by_status,
                             popular_items=popular_items,
                             daily_sales=daily_sales)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

# ==================== RECEPTION: ORDERS ====================
@app.route('/reception/orders')
@role_required('reception', 'admin')
def reception_orders():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get filters
        search = request.args.get('search', '')
        status = request.args.get('status', '')
        
        # Build query
        query = """
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (o.id LIKE %s OR o.customer_name LIKE %s)"
            search_pattern = f'%{search}%'
            params.extend([search_pattern, search_pattern])
        
        if status:
            query += " AND o.status = %s"
            params.append(status)
        
        query += " ORDER BY o.created_at DESC"
        
        cursor.execute(query, params)
        orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('reception/orders.html', orders=orders, search=search, selected_status=status)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

# ==================== KITCHEN: ORDERS ====================
@app.route('/kitchen/orders')
@role_required('kitchen', 'admin')
def kitchen_orders():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get pending and preparing orders
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE o.status IN ('Pending', 'Preparing')
            ORDER BY o.created_at ASC
        """)
        active_orders = cursor.fetchall()
        
        # Get ready orders
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE o.status = 'Ready'
            ORDER BY o.created_at ASC
        """)
        ready_orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return render_template('kitchen/orders.html', active_orders=active_orders, ready_orders=ready_orders)
    
    flash('Database connection error. Please try again later.', 'danger')
    return redirect(url_for('dashboard'))

# ==================== KITCHEN: API FOR REAL-TIME UPDATES ====================
@app.route('/api/kitchen/orders')
@role_required('kitchen', 'admin')
def kitchen_orders_api():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Get active orders
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE o.status IN ('Pending', 'Preparing')
            ORDER BY o.created_at ASC
        """)
        active_orders = cursor.fetchall()
        
        # Get ready orders
        cursor.execute("""
            SELECT o.*, 
                   (SELECT COUNT(*) FROM order_items WHERE order_id = o.id) as item_count
            FROM orders o 
            WHERE o.status = 'Ready'
            ORDER BY o.created_at ASC
        """)
        ready_orders = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'active_orders': active_orders,
            'ready_orders': ready_orders
        })
    
    return jsonify({'error': 'Database connection error'}), 500

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
