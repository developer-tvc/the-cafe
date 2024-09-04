from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.core.signals import request_finished
from django.dispatch import receiver


class AboutCafe(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    cafe_name = models.CharField(max_length=200, blank=True)
    about = models.TextField(max_length=900, null=True, blank=True)
    cafe_time = models.CharField(max_length=200, blank=True)
    cafe_short_address = models.TextField(max_length=500, null=True, blank=True)
    cafe_full_address = models.TextField(max_length=1500, null=True, blank=True)
    phone_no = models.BigIntegerField(blank=True)
    country = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.cafe_name


class Category(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    category_name = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Menu(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    cafe = models.ForeignKey("aboutCafe", on_delete=models.CASCADE)
    category = models.ForeignKey("category", on_delete=models.CASCADE)
    category_name = models.CharField(max_length=300, null=True, blank=True)
    dish_name = models.CharField(max_length=300, null=True, blank=True)
    dish_discription = models.TextField(max_length=500, null=True, blank=True)
    dish_price = models.IntegerField(blank=True, default=0)
    dish_photo = models.ImageField(
        upload_to="thumbnail/", help_text="Image size:370 X 370."
    )
    approval_flag = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.dish_name


class Contact(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    name = models.CharField(max_length=300, null=True, blank=True)
    number_of_People = models.IntegerField(blank=True)
    date_of_booking = models.DateTimeField(blank=True)
    message = models.TextField(max_length=500, null=True, blank=True)
    phone_no = models.BigIntegerField(blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderd = models.BooleanField(blank=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return str(self.user.first_name) + "   " + str(self.total_price)


class CartItem(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    cart = models.ForeignKey("cart", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("Menu", on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    isOrder = models.CharField(max_length=300, null=True, blank=True)
    total_items = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):

        return str(self.product)


@receiver(pre_save, sender=CartItem)
def calculate_price(sender, **kwargs):
    new_cart_items = kwargs["instance"]
    price_of_product = Menu.objects.get(id=new_cart_items.product.id)
    new_cart_items.price = int(new_cart_items.quantity) * int(
        price_of_product.dish_price
    )
