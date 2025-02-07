# FastAPI E-Commerce API

## 🚀 Project Overview
This FastAPI-based e-commerce API provides a structured backend system with authentication, database management, and essential shopping functionalities.

### 📌 Features Implemented
- **User Authentication (JWT-based)**
  - User registration and login
  - JWT token generation and protected endpoints
  - Logout functionality
- **Product & Category Management**
  - CRUD operations for products and categories
  - Filtering and pagination (by category, price, stock availability)
- **Shopping Cart System**
  - Add products to the cart with quantity
  - Update or remove items from the cart
  - View cart with total price calculation
- **Checkout & Order Management**
  - Place an order from the cart
  - Reduce stock after checkout
- **Pagination & Filtering**
  - Paginated product listings
  - Filter products by category, price, and availability

---

## 📂 Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository
```sh
 git clone https://github.com/yourusername/ecommerce-fastapi.git
 cd ecommerce-fastapi
```

### 2️⃣ Create a Virtual Environment
```sh
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the root directory:
```ini
DATABASE_URL=postgresql://postgres:password@localhost:5432/e-commerce-db
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080  # 7 days
ALGORITHM=HS256
JWT_SECRET_KEY=your_jwt_secret_key
JWT_REFRESH_SECRET_KEY=your_refresh_secret_key
```

### 5️⃣ Run Database Migrations
```sh
alembic upgrade head
```

### 6️⃣ Start the FastAPI Server
```sh
uvicorn main:app --reload
```

The API will be available at: **http://127.0.0.1:8000**

---

## 📌 API Endpoints

### 🛠️ **Authentication**
| Method | Endpoint      | Description |
|--------|-------------|-------------|
| POST   | `/signup/`  | Register a new user |
| POST   | `/login/`   | Login & get JWT token |

### 📦 **Product & Category Management**
| Method | Endpoint                | Description |
|--------|-------------------------|-------------|
| POST   | `/products/`            | Create a new product |
| GET    | `/products/`            | List all products (with filtering & pagination) |
| GET    | `/products/{product_id}` | Get details of a specific product |
| PUT    | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |
| POST   | `/categories/`           | Create a new category |
| GET    | `/categories/`           | List all categories |
| PUT    | `/categories/{category_id}` | Update a category |
| DELETE | `/categories/{category_id}` | Delete a category |

### 🛒 **Shopping Cart System**
| Method | Endpoint             | Description |
|--------|----------------------|-------------|
| POST   | `/cart/`             | Add an item to the cart |
| GET    | `/cart/`             | View cart with total price |
| PUT    | `/cart/{cart_item_id}` | Update or remove an item from the cart |

### 🏷 **Checkout & Orders**
| Method | Endpoint      | Description |
|--------|-------------|-------------|
| POST   | `/checkout/` | Place an order from the cart |

---

## 📄 Testing the API
You can test the API using **Swagger UI** or **Postman**:

- **Swagger UI**: Available at **http://127.0.0.1:8000/docs**
- **ReDoc UI**: Available at **http://127.0.0.1:8000/redoc**
- **Postman**: Use the provided endpoints with a JWT token (if required)

---

## 🛠 Future Enhancements
- Implement user roles (Admin, Customer, etc.)
- Add product reviews and ratings
- Integrate payment processing
- Implement order history for users

---



