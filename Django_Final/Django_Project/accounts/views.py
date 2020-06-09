from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Sum
# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, TransactionForm
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, superadmin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			#Added username after video because of error returning customer name if not added
			Customer.objects.create(
				user=user,
				name=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	transactions = Transaction.objects.all()
	total_due = transactions.aggregate(Sum("due_amount"))
	total_paid = transactions.aggregate(Sum("paid_amount"))

	context = {'total_customers':total_customers, 'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending, 'transactions':transactions, 'total_due':total_due,
	'total_paid':total_paid }

	return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def userPage(request):
	#orders = request.user.customer.order_set.all()

	#total_orders = orders.count()
	#delivered = orders.filter(status='Delivered').count()
	#pending = orders.filter(status='Pending').count()

	#print('ORDERS:', orders)

	#context = {'orders':orders, 'total_orders':total_orders,
	#'delivered':delivered,'pending':pending}
	context = {}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def clients(request):
	customers = Customer.objects.all()

	return render(request, 'accounts/clients.html', {'customers':customers})

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def orders(request):
	orders = Order.objects.all()

	return render(request, 'accounts/orders.html', {'orders':orders})

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def transactions(request):
	transactions = Transaction.objects.all()
	total_due = transactions.aggregate(Sum("due_amount"))
	total_paid = transactions.aggregate(Sum("paid_amount"))
	context = {'transactions':transactions, 'total_due':total_due, 'total_paid': total_paid}
	return render(request, 'accounts/transactions.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)
	orders = customer.order_set.all()
	order_count = orders.count()
	context = {'customer':customer, 'orders':orders, 'order_count': order_count}
	return render(request, 'accounts/customer.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def createOrder(request):
	form_order = OrderForm()
	if request.method == 'POST':
		form_order = OrderForm(request.POST)
		if form_order.is_valid():
			form_order.save()
			return redirect('/orders')

	context = {'form_order':form_order}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form_order = OrderForm(instance=order)
	print('ORDER:', order)
	if request.method == 'POST':

		form_order = OrderForm(request.POST, instance=order)
		if form_order.is_valid():
			form_order.save()
			return redirect('/orders')

	context = {'form_order':form_order}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/orders')

	context = {'item':order}
	return render(request, 'accounts/delete_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def createCustomer(request):
	form_customer = CustomerForm()
	if request.method == 'POST':
		form_customer = CustomerForm(request.POST)
		if form_customer.is_valid():
			form_customer.save()
			return redirect('/clients')

	context = {'form_customer':form_customer}
	return render(request, 'accounts/customer_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def updateCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	form_customer = CustomerForm(instance=customer)
	print('Customer:', customer)
	if request.method == 'POST':

		form_customer = CustomerForm(request.POST, instance=customer)
		if form_customer.is_valid():
			form_customer.save()
			return redirect('/clients')

	context = {'form_customer':form_customer}
	return render(request, 'accounts/customer_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == "POST":
		customer.delete()
		return redirect('/clients')

	context = {'item':customer}
	return render(request, 'accounts/delete_customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def createTransaction(request):
	form_transaction = TransactionForm()
	if request.method == 'POST':
		form_transaction = TransactionForm(request.POST)
		if form_transaction.is_valid():
			form_transaction.save()
			return redirect('/transactions')


	context = {'form_transaction':form_transaction}
	return render(request, 'accounts/transaction_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def updateTransaction(request, pk):
	transaction = Transaction.objects.get(id=pk)
	form_transaction = TransactionForm(instance=transaction)
	print('Transaction:', transaction)
	if request.method == 'POST':

		form_transaction = TransactionForm(request.POST, instance=transaction)
		if form_transaction.is_valid():
			form_transaction.save()
			return redirect('/transactions')

	context = {'form_transaction':form_transaction}
	return render(request, 'accounts/transaction_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['superadmin', 'admin', 'chairperson', 'director', 'auditor', 'operator', 'secondman'])
def deleteTransaction(request, pk):
	transaction = Transaction.objects.get(id=pk)
	if request.method == "POST":
		transaction.delete()
		return redirect('/transactions')

	context = {'item':transaction}
	return render(request, 'accounts/delete_transaction.html', context)