from django.contrib import admin

# Register your models here.
from .models import Product, Category, Brand, Images, City, Profile


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'email', 'city', 'number')
    list_display_links = ('id', 'title')
    list_editable = ('number',)
    list_per_page = 10
    search_fields = ('title', 'city', 'email', 'author', 'number')
    list_filter = ('city', 'date')


admin.site.register(Product, ContactAdmin)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Images)
admin.site.register(City)
admin.site.register(Profile)
