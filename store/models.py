from django.db import models




class Category(models.Model):
    name=models.CharField(max_length=100,unique=True)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=255)
    category=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField(default=0)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name


