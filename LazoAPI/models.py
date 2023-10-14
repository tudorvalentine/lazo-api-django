from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=512)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    registered = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Product(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='images/', default='')
    angle1 = models.ImageField(upload_to='images/', default='')
    angle2 = models.ImageField(upload_to='images/', default='')
    angle3 = models.ImageField(upload_to='images/', default='')
    angle4 = models.ImageField(upload_to='images/', default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['rating']


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    order_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order_date']


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ['quantity']


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    address = models.CharField(max_length=200)


class PaymentCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_owner = models.TextField()
    cvv = models.TextField()
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
