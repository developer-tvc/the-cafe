from django.contrib import admin

from pantry.models import AboutCafe, Menu, Category, Contact, Cart, CartItem


admin.site.register(AboutCafe)
admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(Contact)
admin.site.register(Cart)
admin.site.register(CartItem)
