from django.shortcuts import render,redirect
from .models import *
from .forms import OrderForm, CustomerForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@login_required(login_url='login')
@allowed_users(allowd_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    # print("Orders:", orders)
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'orders': orders, 'total_orders': total_orders, 'delivered':
                delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@login_required(login_url='login')
@allowed_users(allowd_roles=['customer'])
def accountSettings(request):
	customer1 = request.user.customer
	form = CustomerForm(instance=customer1)
	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer1)
		if form.is_valid():
			form.save()
	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    delivered = orders.filter(status = 'Delivered').count()
    pending = orders.filter(status = 'Pending').count()
    context = {'orders': orders, 'customers': customers, 'total_orders':total_orders,
              'total_customers': total_customers, 'delivered': delivered,
               'pending':pending}
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowd_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowd_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs
    context = {'customer': customer, 'orders' : orders, 'orders_count':orders_count, 'myfilter': myfilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowd_roles=['admin'])
def create_order(request, pk):
    Orderformset = inlineformset_factory(Customer, Order, fields =('product','status'), extra= 10)
    customer = Customer.objects.get(id=pk)
    formset = Orderformset(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        formset = Orderformset(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowd_roles=['admin'])
def update_order(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'accounts/order_form.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowd_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order':order}
    return render(request, 'accounts/delete_order.html', context)










# @login_required(login_url='login')
# @allowed_users(allowd_roles=['admin'])
# def create_customer(request):
#     form = CustomerForm()
#     if request.method == 'POST':
#         form = CustomerForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     context = {'form': form}
#     return render(request, 'accounts/customer_form.html', context)
#
#
# @login_required(login_url='login')
# @allowed_users(allowd_roles=['admin'])
# def update_customer(request, pk):
#     customer = Order.objects.get(id=pk)
#     form = CustomerForm(instance=customer)
#     if request.method == 'POST':
#         form = CustomerForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('/')
#     return render(request, 'accounts/customer_form.html', {'form': form})





