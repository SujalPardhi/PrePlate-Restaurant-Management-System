# PrePlate - Restaurant Pre-order Platform

**Order Ahead. Pick Up Fresh.**

A complete, professional restaurant and café food pre-order web application that allows customers to browse menus, place orders in advance, and track order status. Restaurant staff can manage menus, orders, and view sales analytics.

## 🌟 Features

### Customer Features
- **User Registration & Authentication** - Secure sign-up and login with password hashing
- **Menu Browsing** - View all food items with images, descriptions, and prices
- **Advanced Search & Filtering** - Search by name/description, filter by category and availability
- **Food Details** - Detailed view of each food item with quantity selection
- **Shopping Cart** - Add items, adjust quantities, remove items, view totals
- **Smart Checkout** - Select pickup date and time with validation
- **Order Confirmation** - Instant confirmation with order ID and details
- **Order Tracking** - Real-time status tracking (Pending → Accepted → Preparing → Ready → Completed)
- **Order History** - View all past and current orders with status
- **Responsive Design** - Works seamlessly on desktop, tablet, and mobile

### Admin Features
- **Professional Dashboard** - Real-time statistics and metrics
- **Order Management** - View, search, filter, and manage all orders
- **Status Updates** - Update order status with visual workflow
- **Menu Management** - Add, edit, delete, and enable/disable food items
- **Category Management** - Create and manage food categories
- **Sales Reports** - Daily sales, order statistics, popular items
- **Analytics** - Orders by status, completion rates, revenue tracking

## 🛠 Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom design
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - Dynamic interactions

### Backend
- **Python 3.x** - Core programming language
- **Flask** - Web framework
- **Werkzeug** - Password hashing and security

### Database
- **MySQL** - Relational database management
- **mysql-connector-python** - Python MySQL driver

### Additional Libraries
- **python-dotenv** - Environment variable management

## 📁 Project Structure

```
PrePlate/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── setup_admin.py             # Admin password setup script
├── .env.example               # Environment variables template
│
├── database/
│   └── schema.sql             # Database schema and seed data
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Home page
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   ├── menu.html              # Menu browsing page
│   ├── food_details.html      # Food item details
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Checkout page
│   ├── order_confirmation.html # Order confirmation
│   ├── my_orders.html         # Customer order history
│   ├── order_details.html     # Order details and tracking
│   ├── 404.html               # 404 error page
│   ├── 500.html               # 500 error page
│   │
│   └── admin/
│       ├── base.html          # Admin base template
│       ├── dashboard.html     # Admin dashboard
│       ├── orders.html        # Order management
│       ├── order_details.html # Order details and status update
│       ├── menu.html          # Menu management
│       ├── add_food.html      # Add new food item
│       ├── edit_food.html     # Edit food item
│       ├── categories.html    # Category management
│       └── reports.html       # Sales reports and analytics
│
├── static/
│   ├── css/
│   │   └── style.css          # Custom CSS styling
│   │
│   ├── js/
│   │   └── script.js          # Custom JavaScript
│   │
│   └── images/                # Food item images
│
└── README.md                  # This file
```

## 🗄 Database Design

### Tables

#### `users`
- User accounts with roles (customer/admin)
- Password hashing for security
- Email uniqueness constraint

#### `categories`
- Food categories for organization
- Used for menu filtering

#### `food_items`
- Menu items with details
- Category foreign key
- Availability status
- Image references

#### `orders`
- Customer orders with pickup scheduling
- Status tracking
- Financial calculations (subtotal, tax, total)

#### `order_items`
- Individual items in each order
- Quantity and price at time of order
- Foreign key relationships

### Relationships
```
users (1:N) → orders (1:N) → order_items (N:1) → food_items (N:1) → categories
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd "C:\PROJECTS\PrePlate Canteen App"
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure MySQL Database

#### 4.1 Create MySQL Database
```sql
CREATE DATABASE preplate_db;
```

#### 4.2 Import Schema
```bash
mysql -u root -p preplate_db < database/schema.sql
```

Or run manually in MySQL:
```sql
USE preplate_db;
source C:/PROJECTS/PrePlate Canteen App/database/schema.sql;
```

### Step 5: Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env  # On Windows
# cp .env.example .env  # On Linux/Mac
```

2. Edit `.env` with your MySQL credentials:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=preplate_db
```

### Step 6: Setup Admin Password

Run the setup script to properly hash the admin password:
```bash
python setup_admin.py
```

This will update the admin password in the database with proper security hashing.

### Step 7: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## 🔐 Default Credentials

### Admin Account
- **Email:** admin@preplate.com
- **Password:** Admin@123

**Important:** Change the default admin password after first login for security.

### Customer Account
Register a new customer account through the registration page.

## 📱 Usage Guide

### Customer Workflow

1. **Register/Login** - Create account or login with existing credentials
2. **Browse Menu** - Explore food items, use search and filters
3. **View Details** - Click on items to see full details
4. **Add to Cart** - Select quantity and add items to cart
5. **Review Cart** - Adjust quantities, remove items, view totals
6. **Checkout** - Select pickup date and time
7. **Place Order** - Confirm order and receive order ID
8. **Track Order** - Monitor order status in real-time
9. **View History** - Access all past orders

### Admin Workflow

1. **Login** - Access admin dashboard with admin credentials
2. **View Dashboard** - Monitor today's statistics and recent orders
3. **Manage Orders** - View, filter, and update order statuses
4. **Update Status** - Change order status through the workflow
5. **Manage Menu** - Add, edit, delete, or toggle food item availability
6. **Manage Categories** - Create and organize food categories
7. **View Reports** - Analyze sales data and popular items

## 🎨 Design Principles

- **Professional & Clean** - Business-oriented, minimal design
- **Modern UI** - Contemporary aesthetics with smooth interactions
- **Responsive** - Optimized for all screen sizes
- **Accessible** - High contrast, clear typography
- **Fast Performance** - Optimized loading and interactions
- **User-Friendly** - Intuitive navigation and workflows

## 🔒 Security Features

- **Password Hashing** - Uses Werkzeug's secure password hashing
- **SQL Injection Prevention** - Parameterized queries throughout
- **Session Management** - Secure Flask session handling
- **Role-Based Access** - Admin-only routes protected
- **Input Validation** - Server-side validation on all forms
- **CSRF Protection** - Built-in Flask CSRF protection
- **User Isolation** - Customers can only access their own orders

## 🧪 Testing

### Manual Testing Checklist

#### Customer Flow
- [ ] Register new customer account
- [ ] Login with customer credentials
- [ ] Browse menu items
- [ ] Search for specific food
- [ ] Filter by category
- [ ] View food details
- [ ] Add item to cart
- [ ] Adjust cart quantities
- [ ] Remove item from cart
- [ ] Proceed to checkout
- [ ] Select pickup time
- [ ] Place order successfully
- [ ] View order confirmation
- [ ] Track order status
- [ ] View order history
- [ ] Logout

#### Admin Flow
- [ ] Login with admin credentials
- [ ] View dashboard statistics
- [ ] View recent orders
- [ ] Filter orders by status
- [ ] Search for specific order
- [ ] View order details
- [ ] Update order status
- [ ] Add new food item
- [ ] Edit existing food item
- [ ] Toggle food availability
- [ ] Add new category
- [ ] View sales reports
- [ ] View popular items
- [ ] Logout

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check MySQL service is running
# Verify credentials in .env file
# Test connection:
mysql -u root -p preplate_db
```

### Port Already in Use
```bash
# Change port in app.py:
if __name__ == '__main__':
    app.run(debug=True, port=5001)
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Password Hash Issues
```bash
# Re-run admin setup
python setup_admin.py
```

## 📊 SQL Operations Demonstrated

The project demonstrates comprehensive SQL operations:
- **INSERT** - Adding users, orders, food items
- **SELECT** - Retrieving data with complex queries
- **UPDATE** - Modifying order status, food availability
- **DELETE** - Removing items (with safety checks)
- **WHERE** - Conditional filtering
- **ORDER BY** - Sorting results
- **GROUP BY** - Aggregation for reports
- **COUNT** - Counting records
- **SUM** - Calculating totals
- **JOIN** - Table relationships (INNER JOIN)
- **LIKE** - Pattern matching for search
- **Aggregate Functions** - Complex analytics

## 🔮 Future Improvements

- [ ] Email notifications for order status changes
- [ ] SMS notifications for pickup reminders
- [ ] Payment gateway integration (Razorpay, Stripe)
- [ ] Multi-restaurant support
- [ ] Customer reviews and ratings
- [ ] Advanced analytics dashboard
- [ ] Mobile app (React Native/Flutter)
- [ ] Loyalty program
- [ ] Promotional codes and discounts
- [ ] Inventory management
- [ ] Staff scheduling
- [ ] QR code ordering
- [ ] API for third-party integrations

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

## 👥 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues, questions, or suggestions:
- Open an issue in the repository
- Contact the development team

## 🙏 Acknowledgments

- Flask web framework
- Bootstrap UI framework
- MySQL database
- Python community

---

**PrePlate - Order Ahead. Pick Up Fresh.**

Built with ❤️ using Flask, Bootstrap 5, and MySQL.
