from django.db import models
from datetime import datetime

director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2,
                                choices=POSITIONS,
                                default=cashier)
    labor_contract = models.IntegerField(default=0)

    def get_last_name(self):
        return self.full_name.split()[0]


class Product(models.Model):
    name=models.CharField(max_length=255)
    price=models.FloatField(default=0.0)

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    pickup = models.BooleanField(default = False)
    complete = models.BooleanField(default = False)
    staff = models.ForeignKey(Staff, on_delete = models.CASCADE)
    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:
            return (self.time_out - self.time_in).total_seconds()//60
        else:
            return (datetime.now(timezone.utc) - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1)

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount


