from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user_page"),

    path('account/', views.accountSettings, name="account"),

    path('products/', views.products, name="products"),
    path('clients/', views.clients, name="clients"),
    path('orders/', views.orders, name="orders"),

    path('transactions/', views.transactions, name="transactions"),
    path('create_transaction/', views.createTransaction, name="create_transaction"),
    path('update_transaction/<str:pk>/', views.updateTransaction, name="update_transaction"),
    path('delete_transaction/<str:pk>/', views.deleteTransaction, name="delete_transaction"),


    path('customer/<str:pk_test>/', views.customer, name="customer"),

    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),


    path('create_customer/', views.createCustomer, name="create_customer"),
    path('update_customer/<str:pk>/', views.updateCustomer, name="update_customer"),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name="delete_customer"),



]