from django.contrib import admin

from .models import Order, User, Brand, Product, Review, OrderItem, Address, PaymentCard


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_products', 'order_date')

    def get_products(self, obj):
        return ", ".join([str(product) for product in obj.products.all()])

    get_products.short_description = 'Products'  # Set the column header in the admin panel


admin.site.register(Order, OrderAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'registered')


admin.site.register(User, UserAdmin)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


admin.site.register(Brand, BrandAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'price', 'brand', 'cover_image')


admin.site.register(Product, ProductAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'comment', 'rating', 'date_added')


admin.site.register(Review, ReviewAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(PaymentCard)
