from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    
CATEGORY_CHOICES = [
        ('Laptops', 'Laptops'),
        ('Headphones', 'Headphones'),
        ('Tablets', 'Tablets'),
        ('Networking', 'Networking'),
        ('PC Gaming', 'PC Gaming'),
    ]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200,blank=False)
    price=models.FloatField(max_length=200,blank=False)
    oldPrice=models.FloatField(max_length=200,blank=False)
    image = models.ImageField(upload_to='products/') 
    discount=models.CharField(max_length=200,default="25% OFF")
    description=models.CharField(max_length=1000,blank=False)
    SecondImage= models.ImageField(upload_to='products/') 
    ThirdImage= models.ImageField(upload_to='products/') 
    FourthImage= models.ImageField(upload_to='products/') 
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Laptops')


    def __str__(self):
        return self.name
    
STATUS_CHOICES = [
        ('Delivered', 'Delivered'),
        ('InTransit', 'InTransit'),
        ('Processing', 'Processing'),
    ]

class OrderedItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ordered_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_items')
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.FloatField(blank=False)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing')

    def __str__(self):
        return f"{self.product.name} ordered by {self.user.email}"

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.price
        super().save(*args, **kwargs)

