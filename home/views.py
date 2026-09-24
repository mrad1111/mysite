from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


from .models import Product, Category, Order, OrderItem, Review , Wishlist, CustomerProfile
from .forms import RegisterForm, ReviewForm, LoginForm, CheckoutForm, ContactForm


def index(request):
    return render(request, "index.html")


def home(request):

    categories = Category.objects.all()
    products = Product.objects.all()

    category_id = request.GET.get("category")
    search = request.GET.get("search")

    if category_id:
        products = products.filter(category_id=category_id)

    if search:
        products = products.filter(name__icontains=search)

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    # Provide wishlist product ids for authenticated users so templates
    # can indicate which products are already wishlisted.
    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True)
        )
    else:
        wishlist_product_ids = set()

    return render(
        request,
        "home.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
            "cart_count": cart_count,
            "wishlist_product_ids": wishlist_product_ids,
        },
    )


def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            CustomerProfile.objects.update_or_create(
                user=user,
                defaults={"phone_number": form.cleaned_data["phone_number"]},
            )

            login(request, user)

            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "register.html",
        {
            "form": form,
        },
    )


def user_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            login(request, form.get_user())

            return redirect("home")

    return render(
        request,
        "login.html",
        {
            "form": form,
        },
    )


def user_logout(request):

    logout(request)

    return redirect("home")


@login_required
def profile(request):

    categories = Category.objects.all()
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    CustomerProfile.objects.get_or_create(user=request.user)
    total_orders = Order.objects.filter(user=request.user).count()
    recent_orders = Order.objects.filter(user=request.user).order_by("-created_at")[:3]
    wishlist_count = Wishlist.objects.filter(user=request.user).count()

    return render(
        request,
        "profile.html",
        {
            "categories": categories,
            "cart_count": cart_count,
            "customer": request.user,
            "total_orders": total_orders,
            "recent_orders": recent_orders,
            "wishlist_count": wishlist_count,
        },
    )


@login_required
def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1

    request.session["cart"] = cart

    return redirect("cart")


@login_required
def order_now(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        return redirect("product_detail", product_id=product.id)

    request.session["cart"] = {str(product_id): 1}

    return redirect("checkout")

def increase_quantity(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session["cart"] = cart

    return redirect("cart")

def decrease_quantity(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:

        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")

def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart

    return redirect("cart")


def cart(request):

    cart = request.session.get("cart", {})

    products = []
    total = 0

    for product_id, quantity in cart.items():

        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        products.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    cart_count = sum(cart.values())

    # Order Summary
    shipping = 0
    discount = 0
    grand_total = total + shipping - discount

    return render(
        request,
        "cart.html",
        {
            "products": products,
            "total": total,
            "cart_count": cart_count,
            "shipping": shipping,
            "discount": discount,
            "grand_total": grand_total,
        },
    )


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    # Toggle wishlist: if exists, remove; otherwise add.
    existing = Wishlist.objects.filter(user=request.user, product=product).first()

    if existing:
        existing.delete()
    else:
        Wishlist.objects.create(user=request.user, product=product)

    # Redirect back to product detail
    return redirect("product_detail", product_id=product.id)

def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items,
            "cart_count": cart_count,
        },
    )

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())
    return render(request, "orders.html", {"orders": orders, "cart_count": cart_count})

@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("cart")

    products = []
    subtotal = Decimal("0")
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        line_total = product.price * quantity
        subtotal += line_total
        products.append({"product": product, "quantity": quantity, "subtotal": line_total})

    shipping = Decimal("0") if subtotal >= Decimal("2000") else Decimal("99")
    discount = Decimal("0")
    coupon_code = ""
    form = CheckoutForm()

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            coupon_code = form.cleaned_data["coupon_code"].strip().upper()
            if coupon_code == "SAVE10":
                discount = subtotal * Decimal("0.10")
            elif coupon_code == "WELCOME20":
                discount = Decimal("200")
            elif coupon_code:
                form.add_error("coupon_code", "Invalid coupon code")
            if not form.errors:
                grand_total = subtotal + shipping - discount
                order = Order.objects.create(user=request.user, total_price=grand_total)
                for item in products:
                    OrderItem.objects.create(order=order, product=item["product"], quantity=item["quantity"])
                request.session.pop("cart", None)
                return render(request, "order_success.html", {"order": order})

    if request.method == "GET" and request.GET.get("coupon"):
        coupon_code = request.GET["coupon"].strip().upper()
        if coupon_code == "SAVE10":
            discount = subtotal * Decimal("0.10")
        elif coupon_code == "WELCOME20":
            discount = Decimal("200")

    grand_total = subtotal + shipping - discount
    categories = Category.objects.all()
    cart_count = sum(cart.values())

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "products": products,
            "subtotal": subtotal,
            "shipping": shipping,
            "discount": discount,
            "grand_total": grand_total,
            "coupon_code": coupon_code,
            "cart_count": cart_count,
            "categories": categories,
        },
    )


def product_detail(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    related_products = Product.objects.exclude(
        id=product.id
    )[:4]

    reviews = Review.objects.filter(product=product)

    form = ReviewForm()

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    if request.user.is_authenticated:
        wishlist_product_ids = set(
            Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True)
        )
    else:
        wishlist_product_ids = set()

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related_products": related_products,
            "reviews": reviews,
            "form": form,
            "cart_count": cart_count,
            "wishlist_product_ids": wishlist_product_ids,
        },
    )


def category_products(request, category_id):

    categories = Category.objects.all()

    products = Product.objects.filter(
        category_id=category_id
    )

    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(
        request,
        "products.html",
        {
            "products": products,
            "categories": categories,
            "cart_count": cart_count,
            "search": "",
            "wishlist_product_ids": set(),
            "is_category_page": True,
        },
    )


def about(request):

    categories = Category.objects.all()
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())

    return render(
        request,
        "about.html",
        {
            "categories": categories,
            "cart_count": cart_count,
        },
    )


def contact(request):

    categories = Category.objects.all()
    cart = request.session.get("cart", {})
    cart_count = sum(cart.values())
    success_message = ""

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            success_message = "Thank you! Your message has been received. We will reply shortly."
            form = ContactForm()
    else:
        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "categories": categories,
            "cart_count": cart_count,
            "form": form,
            "success_message": success_message,
        },
    )