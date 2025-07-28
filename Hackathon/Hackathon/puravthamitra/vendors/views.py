# vendors/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Vendor, Product, CartItem, Order
from suppliers.models import Product


from .models import CartItem  # assuming CartItem is in current app
from suppliers.models import Product  # assuming Product is in suppliers app



from django.shortcuts import redirect, get_object_or_404
from .models import CartItem


# ──────────────── 🔐 Auth Views ────────────────
def vendor_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        Vendor.objects.create(user=user)
        return redirect('vendor_login')
    return render(request, 'vendors/vendor_register.html')


def vendor_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user and Vendor.objects.filter(user=user).exists():
            login(request, user)
            return redirect('vendor_dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a registered vendor.')
    return render(request, 'vendors/login.html')


def home(request):
    return render(request, 'vendors/home.html')


# ──────────────── 📊 Dashboard View ────────────────
#from .models import VendorOrder  # adjust based on your model
@login_required
def vendor_dashboard(request):
    vendor = request.user

    total_orders = Order.objects.filter(vendor=vendor).count()
    completed_orders = Order.objects.filter(vendor=vendor, status='completed').count()
    in_progress_orders = Order.objects.filter(vendor=vendor, status='in_progress').count()

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'in_progress_orders': in_progress_orders,
    }
    return render(request, 'vendors/vendor_dashboard.html', context)


# ──────────────── 🔍 Browse & Cart Views ────────────────

@login_required
def browse_products(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(product_name__icontains=query)
    return render(request, 'vendors/browse_products.html', {'products': products})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)

# from decimal import Decimal
# from django.http import JsonResponse

# @login_required
# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         quantity = int(request.POST.get("quantity", 1))
#         # Example: fetching price from DB
#         product = get_object_or_404(Product, id=product_id)
#         price = product.price
#         total = price * quantity
        
#         return JsonResponse({
#             "message": "Item added successfully",
#             "product_name": product.product_name,
#             "quantity": quantity,
#             "price": float(price),            # ✅ convert Decimal to float
#             "total_price": float(total)       # ✅ convert Decimal to float
#         })

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    for item in cart_items:
        item.total_price = item.quantity * item.product.price_per_kg

    return render(request, 'vendors/view_cart.html', {
        'cart_items': cart_items
    })


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('view_cart')

from suppliers.models import Product
from vendors.models import CartItem, Order

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from vendors.models import CartItem, Order
from suppliers.models import Product
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order
from suppliers.models import Product
from django.utils import timezone

from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from .models import CartItem, Order

@login_required
def confirm_order(request):
    if request.method == 'POST':
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('view_cart')

        order = Order.objects.create(vendor=request.user)
        order.items.set(cart_items)  # ✅ use .set() for ManyToMany
        order.save()

        # Set stock to 0 for ordered products
        for item in cart_items:
            item.product.stock = 0
            item.product.save()

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('my_orders')
    return redirect('view_cart')



# ──────────────── 📦 Order History ────────────────
def my_orders(request):
    orders = Order.objects.filter(vendor=request.user).order_by('-created_at')
    return render(request, 'vendors/my_orders.html', {'orders': orders})


@login_required
def delete_vendor_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, vendor=request.user)

    if order.status == 'completed':
        messages.error(request, "Completed orders cannot be deleted.")
        return redirect('my_orders')

    if request.method == "POST":
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('my_orders')

# def view_cart(request):
#     cart_items = Cart.objects.filter(user=request.user)
#     return render(request, 'vendors/view_cart.html', {'cart_items': cart_items})



@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(vendor=request.user)
    if cart_items.exists():
        order = Order.objects.create(vendor=request.user)
        order.items.set(cart_items)
        order.save()
        cart_items.delete()  # Empty cart
        return redirect('my_orders')
    return redirect('view_cart')