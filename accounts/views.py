from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import Product, Order, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import OrderForm, UserRegisterForm
from .filters import OrderFilter

def register(request):
    form = UserRegisterForm()

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            form.save()
            messages.success(request, f"Account is Created For {username}")
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)
    
def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    context = {}
    return render(request, 'accounts/login.html', context)

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    totalCutomers = customers.count()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders': totalOrders, 'total_customer': totalCutomers, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)

def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'total_orders': total_orders, 'myFilter': myFilter}
    return render(request, 'accounts/customers.html', context)

def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    customer = Customer.objects.get(id=pk)
    Formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        Formset = OrderFormSet(request.POST, instance=customer)

        
        if Formset.is_valid():
            Formset.save()
            return redirect('homepage')
        
    context = {'formset': Formset}
    return render(request, 'components/order_form.html', context)

def update_order(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)

        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'components/order_form.html', context)