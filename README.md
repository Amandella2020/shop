 E-Commerce Backend API (Django REST Framework)
Overview
This is a backend-only e-commerce API built with Django and Django REST Framework.
It provides all core functionalities required for an online shop, including authentication, product management, cart system, order processing, and a mock payment system.
__________________________________________________________________________________
 Features:

 Product Management (Admin)
    •	Create, read, update, and delete products
    •	Includes name, description, price, image, and stock

User Authentication (JWT)
    •	Register new users
    •	Login with JWT authentication
    •	Token refresh support

Shopping Cart
    •	Add items to cart
    •	Update item quantity
    •	Remove items from cart
    •	Automatically merges quantities for the same product

Order System
    •	Create orders
    •	Each order contains product, quantity, and total price
    •	Orders are tied to authenticated users

Mock Payment Endpoint
    •	Simulates payment processing
    •	Random success/failure response
    •	Updates order payment status (pending → paid)
    •	Generates fake transaction reference

Order History
    •	Users can view their past orders

Tech Stack
    •	Python
    •	Django
    •	Django REST Framework
    •	JWT Authentication (SimpleJWT)
    •	SQLite (default database)

Installation
    1.	Clone the repository:
        git clone https://github.com/Amandella2020/shop.git
        cd shop

    2.	Create virtual environment:
        python -m venv venv
        source venv/bin/activate   # Windows: venv\Scripts\activate 

    3.	Install dependencies:
        pip install -r requirements.txt

    4.	Run migrations:
        python manage.py makemigrations
        python manage.py migrate
        
    5.	Start server:
        python manage.py runserver


Authentication Endpoints

    Register User
    POST /shopapi/users/

    Login (Get Tokens)
    POST /shopapi/token/

    Refresh Token
    POST /shopapi/token/refresh/

Product Endpoints
    GET     /shopapi/products/
    POST    /shopapi/products/
    GET     /shopapi/products/<id>/
    PUT     /shopapi/products/<id>/
    PATCH   /shopapi/products/<id>/
    DELETE  /shopapi/products/<id>/

Cart Endpoints
    View Cart
    GET /shopapi/cart/
    Add to Cart
    POST /shopapi/cart/add/
    Body:
    {
      "product_id": 1,
      "quantity": 2
    }

    Update Quantity
    PATCH /shopapi/cart/<cart_item_id>/update_quantity/

    Remove Item
    DELETE /shopapi/cart/<cart_item_id>/remove/

Order Endpoints
    Create Order
    POST /shopapi/order/
    Body:
    {
      "product": 1,
      "quantity": 2
    }
    Get Orders
    GET /shopapi/order/
    Delete Order
    DELETE /shopapi/order/<id>/

Mock Payment Endpoint
    Pay for an Order
    POST /shopapi/order/<id>/pay/
    Response (Success):
    {
      "message": "Payment successful",
      "order_id": 1,
      "amount": 5000,
      "payment_ref": "random-uuid",
      "status": "paid"
    }
    Response (Failure):
    {
      "message": "Payment failed",
      "order_id": 1,
      "status": "pending"
    }

Authorization
    All protected endpoints require:
    Authorization: Bearer <access_token>

Design Notes
    •	Orders are created per request (not merged)
    •	Cart handles quantity merging logic
    •	Payment is simulated (no real gateway)
    •	User is automatically attached to requests using JWT

Future Improvements
    •	Checkout endpoint (cart → order)
    •	Real payment integration (Stripe/Paystack)
    •	Product categories
    •	Pagination & filtering
    •	Admin dashboard


Author
    Built by Azuka Nnadi

License
    This project is for educational purposes.

