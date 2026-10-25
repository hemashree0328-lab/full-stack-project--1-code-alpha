from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail

from .models import Product, Order, Category, Review
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Order, Product


# =========================================================
# ORDER CONFIRMATION EMAIL
# =========================================================

def send_order_confirmation_email(order):
    subject = f"Hema Store - Order Confirmation #{order.id}"

    message = f"""
Hello {order.name},

Thank you for shopping with Hema Store!

Your order has been placed successfully.

Order Number: #{order.id}
Order Amount: Rs. {order.total_amount}
Order Status: {order.status}

Delivery Address:
{order.address}

Thank you for choosing Hema Store!
Hema Store Team
"""

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=[order.email],
            fail_silently=False,
        )
        print(f"Order confirmation email sent for Order #{order.id}")
    except Exception as error:
        print(f"Order confirmation email failed: {error}")


# =========================================================
# PRODUCT LIST + SEARCH + CATEGORY FILTER
# =========================================================

def product_list(request):
    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")

    products = Product.objects.all()
    categories = Category.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        "store/products.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
            "selected_category": category_id,
        },
    )


# =========================================================
# PRODUCT DETAILS
# =========================================================

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    reviews = Review.objects.filter(product=product).order_by("-created_at")

    return render(
        request,
        "store/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
        },
    )


# =========================================================
# ADD TO CART
# =========================================================

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect("product_detail", product_id=product.id)

    cart = request.session.get("cart", {})
    product_id = str(product_id)
    current_quantity = cart.get(product_id, 0)

    if current_quantity < product.stock:
        cart[product_id] = current_quantity + 1
        messages.success(request, "Product added to cart.")
    else:
        messages.error(request, "You have reached the available stock limit.")

    request.session["cart"] = cart
    return redirect("cart")


# =========================================================
# INCREASE QUANTITY
# =========================================================

def increase_quantity(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] < product.stock:
            cart[product_id] += 1
        else:
            messages.error(request, "No more stock available.")

    request.session["cart"] = cart
    return redirect("cart")


# =========================================================
# DECREASE QUANTITY
# =========================================================

def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1

    request.session["cart"] = cart
    return redirect("cart")


# =========================================================
# REMOVE FROM CART
# =========================================================

def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    return redirect("cart")


# =========================================================
# CART PAGE
# =========================================================

def cart_view(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

        total += subtotal

    return render(
        request,
        "store/cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


# =========================================================
# REGISTER
# =========================================================

def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            return render(
                request,
                "store/register.html",
                {"error": "Please enter a username and password."},
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "store/register.html",
                {"error": "Username already exists. Choose another username."},
            )

        user = User.objects.create_user(
            username=username,
            password=password,
        )
        login(request, user)
        return redirect("product_list")

    return render(request, "store/register.html")


# =========================================================
# LOGIN
# =========================================================

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("product_list")

        return render(
            request,
            "store/login.html",
            {"error": "Invalid username or password."},
        )

    return render(request, "store/login.html")


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):
    logout(request)
    return redirect("product_list")


# =========================================================
# CHECKOUT + ORDER CONFIRMATION EMAIL
# =========================================================

@login_required(login_url="login")
def checkout(request):
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

        total += subtotal

    if request.method == "POST":
        if not cart:
            messages.error(request, "Your cart is empty.")
            return redirect("cart")

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)

            if quantity > product.stock:
                return render(
                    request,
                    "store/checkout.html",
                    {
                        "cart_items": cart_items,
                        "total": total,
                        "error": (
                            f"Only {product.stock} {product.name} "
                            "available in stock."
                        ),
                    },
                )

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()

        if not all([name, email, phone, address]):
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "error": "Please fill in all checkout fields.",
                },
            )

        order = Order.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            address=address,
            total_amount=total,
        )

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            product.stock -= quantity
            product.save()

        request.session["cart"] = {}
        send_order_confirmation_email(order)

        return redirect("order_success", order_id=order.id)

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
        },
    )


# =========================================================
# ORDER SUCCESS
# =========================================================

@login_required(login_url="login")
def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/order_success.html",
        {"order": order},
    )


# =========================================================
# MY ORDERS
# =========================================================

@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "store/my_orders.html",
        {"orders": orders},
    )


# =========================================================
# TRACK ORDER
# =========================================================

@login_required(login_url="login")
def track_order(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "store/track_order.html",
        {"order": order},
    )


# =========================================================
# ADD OR UPDATE PRODUCT REVIEW
# =========================================================

@login_required(login_url="login")
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method != "POST":
        return redirect("product_detail", product_id=product.id)

    rating = request.POST.get("rating")
    comment = request.POST.get("comment", "").strip()

    if rating not in ["1", "2", "3", "4", "5"]:
        messages.error(request, "Please select a valid star rating.")
        return redirect("product_detail", product_id=product.id)

    if not comment:
        messages.error(request, "Please enter a review comment.")
        return redirect("product_detail", product_id=product.id)

    review, created = Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            "rating": int(rating),
            "comment": comment,
        },
    )

    if created:
        messages.success(request, "Thank you! Your review was added.")
    else:
        messages.success(request, "Your review has been updated.")

    return redirect("product_detail", product_id=product.id)


# =========================================================
# CANCEL ORDER
# =========================================================

@login_required(login_url="login")
def cancel_order(request, order_id):
    if request.method != "POST":
        return redirect("my_orders")

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    if order.status.lower() == "pending":
        order.status = "Cancelled"
        order.save()
        messages.success(
            request,
            "Your order has been cancelled successfully.",
        )
    else:
        messages.error(
            request,
            "Only pending orders can be cancelled.",
        )

    return redirect("my_orders")
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render



from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import render


@staff_member_required
def admin_dashboard(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()

    total_sales = (
        Order.objects.filter(status="delivered")
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    low_stock_products = Product.objects.filter(stock__lte=5)

    monthly_sales = (
        Order.objects.filter(status="delivered")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    order_statuses = (
        Order.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("status")
    )

    context = {
        "total_products": total_products,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "total_sales": total_sales,
        "low_stock_products": low_stock_products,
        "monthly_sales": list(monthly_sales),
        "order_statuses": list(order_statuses),
    }

    return render(request, "store/admin_dashboard.html", context)
