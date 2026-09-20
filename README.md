# PrePlate - Restaurant Order, Kitchen & Sales Management System

**Restaurant Operations System for Efficient Order Management**

A complete internal restaurant management system where staff (not customers) manage orders. Reception staff enter customer orders, kitchen staff prepare food, and customers collect from the counter. Features real-time dashboards, stock management, and public order status display.

## 🌟 Features

### Staff Roles & Access
- **Admin/Owner** - Full control over menu, staff, orders, and sales
- **Reception/Cashier** - Create orders, manage customer pickups, complete orders
- **Kitchen Staff** - View order queue, update preparation status, mark orders ready

### Reception Features
- **Quick Order Entry** - Search and filter food items for fast order creation
- **Stock Validation** - Automatic stock checking before order confirmation
- **Customer Management** - Enter customer name and table number
- **Order Tracking** - View all orders and their current status
- **Real-time Updates** - Dashboard auto-refreshes every 5 seconds

### Kitchen Features
- **Order Queue** - View pending and preparing orders
- **Status Management** - Update order status (Pending → Preparing → Ready)
- **Preparation Time Tracking** - See estimated prep time for each order
- **Real-time Updates** - Dashboard auto-refreshes every 5 seconds
- **Order Details** - View complete order information

### Admin Features
- **Professional Dashboard** - Today's orders, sales, stock statistics
- **Menu Management** - Add, edit, delete food items with stock and prep time
- **Category Management** - Organize food items by category
- **Stock Management** - Monitor and update stock quantities
- **Staff Management** - Add/remove staff accounts, manage roles
- **Sales Reports** - Daily sales, popular items, revenue tracking
- **Order Management** - View all orders, filter by status/date

### Public Display Features
- **Customer-Facing Dashboard** - Shows active orders on restaurant screen
- **Real-Time Status** - Auto-refreshes every 10 seconds
- **Order Priority** - Ready orders shown first for customer attention
- **Ready Notifications** - "🎉 Ready! Collect from counter" message
- **8-Order Limit** - Shows 8 orders at a time (4 per row) for clean display
- **Auto-Removal** - Orders disappear when completed/collected

### Inventory & Stock
- **Stock Tracking** - Automatic stock reduction on order confirmation
- **Out of Stock Prevention** - Blocks orders when stock is zero
- **Stock Alerts** - Visual indicators for low stock items
- **Preparation Time** - Set prep time for each menu item

### Real-Time Features
- **Auto-Refresh Dashboards** - Staff dashboards refresh every 5 seconds
- **Public Display Auto-Refresh** - Customer display refreshes every 10 seconds
- **Instant Order Visibility** - New orders appear immediately on kitchen dashboard
- **Live Status Updates** - Order status changes show instantly across all dashboards

## 🛠 Technology Stack

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom design
- **Bootstrap 5** - Responsive UI framework
- **Vanilla JavaScript** - Dynamic interactions and auto-refresh

### Backend
- **Python 3.x** - Core programming language
- **Flask 3.0.0** - Web framework
- **Werkzeug** - Password hashing and security

### Database
- **MySQL 8.0+** - Relational database management
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
│   ├── schema.sql             # Database schema
│   └── reset_database.sql     # Fresh database reset script
│
├── templates/
│   ├── base.html              # Base template with navigation
│   ├── login.html             # Login page
│   ├── public_dashboard.html   # Public order status display
│   ├── 404.html               # 404 error page
│   ├── 500.html               # 500 error page
│   │
│   ├── admin/                  # Admin templates
│   │   ├── base.html          # Admin base template
│   │   ├── dashboard.html     # Admin dashboard
│   │   ├── orders.html        # Order management
│   │   ├── order_details.html # Order details
│   │   ├── menu.html          # Menu management
│   │   ├── add_food.html      # Add new food item
│   │   ├── edit_food.html     # Edit food item
│   │   ├── categories.html    # Category management
│   │   ├── reports.html       # Sales reports
│   │   └── staff.html        # Staff management
│   │
│   ├── reception/             # Reception staff templates
│   │   ├── dashboard.html     # Reception dashboard
│   │   ├── new_order.html    # Create new order
│   │   ├── orders.html        # View all orders
│   │   └── order_details.html # Order details
│   │
│   └── kitchen/               # Kitchen staff templates
│       ├── dashboard.html     # Kitchen dashboard
│       ├── orders.html        # Kitchen order queue
│       └── order_details.html # Order details with status update
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
- Staff accounts with roles (admin, reception, kitchen)
- Password hashing for security
- Email uniqueness constraint

#### `categories`
- Food categories for organization
- Used for menu filtering

#### `food_items`
- Menu items with details
- Stock quantity tracking
- Preparation time in minutes
- Availability status
- Category foreign key
- Image references

#### `orders`
- Customer orders with customer name and table number
- Status tracking (Pending → Preparing → Ready → Completed)
- Financial calculations (subtotal, total)
- Estimated preparation time
- Created by staff member

#### `order_items`
- Individual items in each order
- Quantity and price at time of order (price snapshot)
- Foreign key relationships

#### `daily_sales`
- Daily sales aggregation
- Total orders, completed orders, items sold
- Total revenue tracking

### Relationships
```
users (1:N) → orders (1:N) → order_items (N:1) → food_items (N:1) → categories
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- MySQL 8.0 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/SujalPardhi/PrePlate-Restaurant-Management-System.git
cd PrePlate-Restaurant-Management-System
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
Open MySQL Workbench or MySQL Command Line and run:
```sql
CREATE DATABASE preplate_db;
```

#### 4.2 Import Schema (Fresh Setup)
For a fresh installation, run the reset script:
```bash
mysql -u root -p < database/reset_database.sql
```

Or manually in MySQL Workbench:
1. Open `database/reset_database.sql`
2. Copy all SQL
3. Paste in MySQL Workbench query window
4. Execute (lightning bolt icon)

This will create a fresh database with:
- 3 staff accounts (admin, reception, kitchen)
- 8 food categories
- 24 sample food items with stock and prep times

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

### Step 6: Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## 🔐 Default Credentials

### Admin Account
- **Email:** admin@preplate.com
- **Password:** Admin@123

### Reception Staff
- **Email:** reception@preplate.com
- **Password:** Admin@123

### Kitchen Staff
- **Email:** kitchen@preplate.com
- **Password:** Admin@123

**Important:** Change default passwords after first login for security.

## 📱 Usage Guide

### Restaurant Workflow

1. **Reception/Cashier** creates order:
   - Login as reception staff
   - Go to "New Order"
   - Enter customer name and table number
   - Search/filter food items
   - Select items and quantities
   - Confirm order
   - Stock automatically reduces

2. **Kitchen** receives order:
   - Order appears automatically on kitchen dashboard (5s refresh)
   - Kitchen sees order details and prep time
   - Kitchen updates status to "Preparing"
   - Kitchen updates status to "Ready"

3. **Customer** sees status:
   - Public dashboard shows order status (10s refresh)
   - When "Ready", message shows: "🎉 Ready! Collect from counter"
   - Customer goes to counter to collect

4. **Reception** completes order:
   - Order marked "Ready" appears on reception dashboard
   - Customer collects order
   - Reception marks order "Completed"
   - Order removed from public display
   - Sales data updated automatically

### Staff Dashboards

#### Reception Dashboard
- View pending and ready orders
- Create new orders
- Track order status
- Complete orders when customer collects

#### Kitchen Dashboard
- View pending orders queue
- Update preparation status
- Mark orders ready
- Auto-refreshes every 5 seconds

#### Admin Dashboard
- View all statistics
- Manage menu and stock
- Manage staff accounts
- View sales reports
- Access all system features

### Public Display Screen
For restaurant TV/customer display:
- Open: http://127.0.0.1:5000/public
- Press F11 for full-screen mode
- Shows 8 orders at a time (4 per row)
- Auto-refreshes every 10 seconds
- Orders disappear when completed

## 🎨 Design Principles

- **Professional & Clean** - Business-oriented, minimal design
- **Restaurant-Focused** - Optimized for restaurant operations
- **High Visibility** - Large text for display screens
- **Color-Coded Status** - Yellow (Pending), Blue (Preparing), Green (Ready)
- **Fast Performance** - Auto-refresh without full page reload where possible
- **Intuitive** - Easy for staff to use during busy hours

## 🔒 Security Features

- **Password Hashing** - Uses Werkzeug's secure password hashing
- **SQL Injection Prevention** - Parameterized queries throughout
- **Session Management** - Secure Flask session handling
- **Role-Based Access** - Staff roles protected (admin, reception, kitchen)
- **Input Validation** - Server-side validation on all forms
- **Transaction Safety** - Database transactions for order creation and stock updates
- **Stock Validation** - Prevents overselling with stock checks

## 🧪 Testing

### Manual Testing Checklist

#### Reception Flow
- [ ] Login as reception staff
- [ ] Create new order with customer name
- [ ] Search and filter food items
- [ ] Select multiple items with quantities
- [ ] Confirm order successfully
- [ ] Verify stock reduced
- [ ] View order in orders list
- [ ] See order status updates
- [ ] Complete order when customer collects

#### Kitchen Flow
- [ ] Login as kitchen staff
- [ ] View pending orders on dashboard
- [ ] See new orders appear automatically
- [ ] Update order status to "Preparing"
- [ ] Update order status to "Ready"
- [ ] View order details
- [ ] Auto-refresh works (5 seconds)

#### Admin Flow
- [ ] Login as admin
- [ ] View dashboard statistics
- [ ] Add new food item with stock and prep time
- [ ] Edit existing food item
- [ ] Update stock quantity
- [ ] Add reception staff account
- [ ] Add kitchen staff account
- [ ] View sales reports
- [ ] View popular items
- [ ] Manage categories

#### Public Display Flow
- [ ] Open public dashboard on browser
- [ ] See active orders (max 8)
- [ ] See order status changes (10s refresh)
- [ ] See "Ready" message when order is ready
- [ ] See order disappear when completed
- [ ] Verify 4 orders per row layout

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

### Login Issues
- Ensure database was created with reset_database.sql
- Verify default credentials are correct
- Check .env file has correct MySQL credentials

### Order Creation Error
- Check if food items have stock > 0
- Verify database schema is updated
- Check MySQL connection

### Public Display Not Updating
- Ensure JavaScript is enabled in browser
- Check auto-refresh script is loading
- Verify database has active orders

## 📊 SQL Operations Demonstrated

The project demonstrates comprehensive SQL operations:
- **INSERT** - Adding orders, food items, staff accounts
- **SELECT** - Retrieving data with complex queries and joins
- **UPDATE** - Modifying order status, stock quantities
- **DELETE** - Removing staff (with safety checks)
- **WHERE** - Conditional filtering by status, date, etc.
- **ORDER BY** - Sorting by priority (Ready → Preparing → Pending)
- **GROUP BY** - Aggregation for sales reports
- **COUNT** - Counting orders and items
- **SUM** - Calculating totals and revenue
- **JOIN** - Table relationships (INNER JOIN, LEFT JOIN)
- **LIKE** - Pattern matching for search
- **CASE** - Conditional sorting for order priority
- **LIMIT** - Limiting results (8 orders for public display)
- **TRANSACTION** - Database transactions for data integrity
- **Aggregate Functions** - Complex analytics and reporting

## 🔮 Future Improvements

- [ ] Email notifications for low stock alerts
- [ ] SMS notifications for order ready (customer)
- [ ] Receipt printing integration
- [ ] Table management and reservation system
- [ ] Advanced analytics dashboard with charts
- [ ] Mobile app for staff (React Native/Flutter)
- [ ] Customer loyalty program
- [ ] Promotional codes and discounts
- [ ] Kitchen display screen with detailed order info
- [ ] Multi-location restaurant support
- [ ] API for third-party integrations (POS systems)

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

**PrePlate - Restaurant Order, Kitchen & Sales Management System**

Built with ❤️ using Flask, Bootstrap 5, and MySQL.
