from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import RegisterForm, CheckoutForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer


@api_view(['GET'])
def product_api(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    request.session['cart'] = cart
    return redirect('view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    final_amount = 0

    for id in cart:
        product = get_object_or_404(Product, id=id)
        quantity = cart[id]
        total = product.price * quantity
        final_amount += total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'final_amount': final_amount
    })


def increase(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart
    return redirect('view_cart')


def decrease(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] -= 1
        if cart[id] <= 0:
            del cart[id]

    request.session['cart'] = cart
    return redirect('view_cart')


def remove(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('view_cart')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('product_list')

    final_total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        final_total += product.price * quantity

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total_amount=final_total)

            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            request.session['cart'] = {}
            return redirect('product_list')
    else:
        form = CheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form, 
        'final_total': final_total
    })


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()

    # Correct template path
    return render(request, 'store/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')

def order_details(request,id):
    order=order.objects.get(id=id,user=request.user)
    return render(request,'store/order.html',{'order':order})
def order_success(request,id):
    order=order.objects.get(id=id,user=request.user)
    return render(request,'store/order_success.html',{'order':order})


def product_list(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.all()
    return render(request,'store/product_list.html',{'products':products})
       