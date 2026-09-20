# Quick Start Guide - PrePlate

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database
```bash
# Create database
mysql -u root -p -e "CREATE DATABASE preplate_db;"

# Import schema
mysql -u root -p preplate_db < database/schema.sql
```

### 3. Configure Environment
```bash
# Copy example env file
copy .env.example .env

# Edit .env with your MySQL credentials
# DB_HOST=localhost
# DB_USER=root
# DB_PASSWORD=your_password
# DB_NAME=preplate_db
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the Application
- **Customer:** http://127.0.0.1:5000
- **Admin:** http://127.0.0.1:5000/admin

### 6. Login Credentials
- **Admin Email:** admin@preplate.com
- **Admin Password:** Admin@123

## 📝 First Steps

### For Testing as Customer:
1. Go to http://127.0.0.1:5000/register
2. Create a new customer account
3. Browse the menu and add items to cart
4. Place an order and track the status

### For Testing as Admin:
1. Login with admin credentials
2. View the dashboard statistics
3. Manage incoming orders
4. Add/edit menu items
5. View sales reports

## 🐛 Common Issues

### MySQL Connection Error
- Ensure MySQL service is running
- Check credentials in .env file
- Verify database name is correct

### Port Already in Use
- Change port in app.py: `app.run(debug=True, port=5001)`

### Import Errors
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## 📚 More Information
See the full [README.md](README.md) for detailed documentation.
