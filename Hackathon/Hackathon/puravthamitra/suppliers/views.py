from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SupplierRegistrationForm
from .models import SupplierProfile

from django.contrib.auth import logout
from .models import *
from .forms import *


def supplier_register(request):
    if request.method == 'POST':
        form = SupplierRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken.")
            else:
                user = User.objects.create_user(username=username, password=password)
                supplier = form.save(commit=False)
                supplier.user = user
                supplier.save()
                messages.success(request, "Registration successful. You can now login.")
                return redirect('supplier_login')
    else:
        form = SupplierRegistrationForm()
    return render(request, 'suppliers/register.html', {'form': form})

def supplier_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            if SupplierProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect('supplier_dashboard')
            else:
                messages.error(request, 'You are not registered as a Supplier.')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'suppliers/login.html')


def dashboard(request):
    # Filter today's orders, pending orders etc.
    return render(request, 'suppliers/dashboard.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Product
@login_required
def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category = request.POST.get('category')
        price_per_kg = request.POST.get('price_per_kg')
        quantity = request.POST.get('quantity')
        image = request.FILES.get('image')
        location = request.POST.get('location')  # <- add this line

        product = Product(
            product_name=product_name,
            category=category,
            price_per_kg=price_per_kg,
            quantity=quantity,
            image=image,
            location=location,  # <- and this line
            supplier=request.user
        )
        product.save()
        return redirect('inventory')

    return render(request, 'suppliers/add_product.html')





# views.py
from .models import Product

def inventory(request):
    products = Product.objects.filter(supplier=request.user)
    return render(request, 'suppliers/inventory.html', {'inventory': products})



from .models import Order  # Assuming Order is your model

@login_required
def orders(request):
    orders = Order.objects.all()  # or apply other filters if needed
    return render(request, 'suppliers/orders.html', {'orders': orders})




from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def mark_delivered(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, supplier=request.user)
        order.status = 'delivered'
        order.save()
        messages.success(request, "Order marked as delivered.")
    return redirect('orders')


from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def account(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email') or user.email
        user.first_name = request.POST.get('first_name') or user.first_name
        user.last_name = request.POST.get('last_name') or user.last_name
        user.save()
        messages.success(request, "Profile updated successfully.")
    
    return render(request, 'suppliers/account.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

@login_required
def history(request):
    rejected_orders = Order.objects.filter(product__supplier=request.user, status='rejected')
    return render(request, 'suppliers/history.html', {'rejected_orders': rejected_orders})


from vendors.models import Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('supplier_login')  # Use correct URL name of your login page



from django.shortcuts import get_object_or_404, redirect
from .forms import ProductForm
from .models import Product


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ProductForm(instance=product)
    return render(request, 'suppliers/edit_product.html', {'form': form})


@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, id=id, supplier=request.user)

    if request.method == "POST":
        product.delete()
        return redirect('inventory')

    return render(request, 'suppliers/delete_product.html', {'product': product})


@login_required
def dashboard(request):
    my_orders = Order.objects.filter(items__product__supplier=request.user).distinct()
    return render(request, 'suppliers/dashboard.html', {'my_orders': my_orders})

@login_required
def supplier_dashboard(request):
    new_orders = Order.objects.filter(vendor=request.user, status='In Process')
    today_deliveries = Order.objects.filter(vendor=request.user, status='Completed')

    context = {
        'new_orders': new_orders,
        'today_deliveries': today_deliveries
    }
    return render(request, 'suppliers/supplier_dashboard.html', context)
