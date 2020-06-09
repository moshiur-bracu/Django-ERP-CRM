from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.

class Customer(models.Model):
	STATUS = (
			('Active', 'Active'),
			('Inactive', 'Inactive'),
			)
	#user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	customer_id = models.CharField(max_length=5, null=True)
	name = models.CharField(max_length=30, null=True)
	phone = models.CharField(max_length=11, null=True)
	email = models.CharField(max_length=30, null=True)
	address = models.CharField(max_length=50, null=True)
	contact_person = models.CharField(max_length=30, null=True)
	profile_pic = models.ImageField(default="profile1.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=10, choices=STATUS, null=True)


	def __str__(self):
		return self.name


class Tag(models.Model):
	name = models.CharField(max_length=10, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	CATEGORY = (
			('Hot & Cold Cup', 'Hot & Cold Cup'),
			('Ice Cream Cup', 'Ice Cream Cup'),
			('Bowl', 'Bowl'),
			('Plate & Tray', 'Plate & Tray'),
			('Muffin Cup', 'Muffin Cup'),
			('Cup with Lid Jacket', 'Cup with Lid Jacket'),
			('Food Box', 'Food Box'),
			('Cup with Handle', 'Cup with Handle'),
			) 
	ML = (
		(' ', ' '),
		('80 ML ', '80 ML '),
		('100 ML ', '100 ML '),
		('130 ML ', '130 ML '),
		('150 ML ', '150 ML '),
		('200 ML ', '200 ML '),
		('225 ML ', '225 ML '),
		('250 ML ', '250 ML '),
		('350 ML ', '350 ML '),
		)
	INCHES = (
		(' ', '  '),
		('7 inches ', '7 inches '),
		('9 inches ', '9 inches '),
		)
	category = models.CharField(max_length=30, null=True, choices=CATEGORY)
	size_ml = models.CharField(max_length=10, null=True, choices = ML)
	size_inches = models.CharField(max_length=10, null=True, choices = INCHES)
	price = models.FloatField(null=True)
	description = models.CharField(max_length=100, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)
	name = models.CharField(max_length=30, null=True)


	def __str__(self):
		return self.name




class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)

	customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
	product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=200, null=True, choices=STATUS)

	def __str__(self):
		return self.product.name


class Transaction(models.Model):
	TYPE = (
			('Cash', 'Cash'),
			('Cheque', 'Cheque'),
			)
	#user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	transaction_id = models.CharField(max_length=5, null=True)
	transaction_type = models.CharField(max_length=10, choices=TYPE, null=True)
	date = models.DateField(auto_now_add=True, null=True)
	customer_id = models.CharField(max_length=6, null=True)
	customer_name = models.CharField(max_length=30, null=True)
	due_amount = models.FloatField(null=True)
	paid_amount = models.FloatField(null=True)
	


	def __str__(self):
		return self.customer_name