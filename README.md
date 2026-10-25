# full-stack-project--1-code-alpha
Django-based e-commerce website with product listings, shopping cart, checkout, order tracking, and admin dashboard.
# Hema Store – Django E-Commerce Website

Hema Store is a web-based e-commerce application developed using Django, Python, HTML, CSS, JavaScript, and SQLite. It allows users to browse products, manage a shopping cart, place orders, and track their order status.

## 🚀 Features

- User registration and login
- Product listing and product details
- Product search
- Add to cart and update product quantities
- Checkout and order processing
- Order history and order tracking
- Order cancellation
- Product reviews
- Admin dashboard with charts
- Low-stock monitoring
- Responsive user interface

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Django
- **Database:** SQLite
- **Tools:** VS Code, Git, GitHub

## 📂 Project Structure

```text
ecommerce_project/
├── ecommerce/
├── store/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── README.md
└── .gitignore
```

*Note: The folder structure may vary depending on your project setup.*

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hema-store.git
cd hema-store
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## 🔐 Admin Access

To create an administrator account, run:

```bash
python manage.py createsuperuser
```

Then visit `http://127.0.0.1:8000/admin/`.

## 🎯 Project Objective

The objective of Hema Store is to demonstrate full-stack web development using Django, including user authentication, product management, shopping cart functionality, order processing, and administrative features.

## 👩‍💻 Author

**Hemashree B.**

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
