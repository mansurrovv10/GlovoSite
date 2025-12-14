from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    ROLE_CHOICES = (
    ('client', 'client'),
    ('courier', 'courier'),
    ('owner', 'owner'),
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=100, default='client')
    date_registered = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=100,unique=True)
    def __str__(self):
        return f'{self.category_name}'


class Store(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='category_store')
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    store_image = models.ImageField(upload_to="store_photos")
    description = models.TextField()
    created_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.store_name}'

    def get_avg_rating(self):
        reviews = self.review_store.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(),1)
        return 0

    def get_count_people(self):
        ratings = self.review_store.all()
        if ratings.exists():
            if ratings.count() > 3:
                return '3+'
            return ratings.count()
        return 0


    def get_avg_procent(self):
        reviews = self.review_store.all()
        count_person = 0
        if reviews.exists():
            for i in reviews:
                if i.rating > 3:
                    count_person+=1
                continue
            return f'{round((count_person * 100) / reviews.count(),1)}%'

        return '0%'






class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='contact_store')
    contact_name = models.CharField(max_length=25)
    contact_number = PhoneNumberField()
    def __str__(self):
        return f'{self.contact_name}, {self.contact_number}'


class Address(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='address_store')
    address_name = models.CharField(max_length=75)
    def __str__(self):
        return self.address_name


class StoreMenu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE,related_name='store_menu_store')
    menu_name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.menu_name}'


class Product(models.Model):
    store = models.ForeignKey(StoreMenu, on_delete=models.CASCADE,related_name='menu_store')
    product_name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to="product_photos")
    product_description = models.TextField()
    product_price = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return f'{self.product_name},{self.store}'

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='client_order')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='courier_order')
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    StatusChoices = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    status = models.CharField(choices=StatusChoices, max_length=100, default='Pending')
    delivery_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.client}, {self.products}, {self.status}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='current_orders')
    CourierStatus = (
        ('Busy', 'Busy'),
        ('Available', 'Available'),
    )
    courier_status = models.CharField(choices=CourierStatus, max_length=100)
    def __str__(self):
        return f'{self.user},{self.courier_status}'

class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='review_client')
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE,related_name='review_courier',
                                null=True, blank=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE,null=True,blank=True,related_name='review_store')
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.client}, {self.rating}'

