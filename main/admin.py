from django.contrib import admin
from .models import Item, CartItems
from django.db import models

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Title", {'fields': ["title"]}),
        ("Image", {'fields': ["image"]}),
        ("Description", {'fields': ["description"]}),
        ("Price", {'fields': ["price"]}),
        ("Pieces", {'fields': ["pieces"]}),
        ("Instructions", {'fields': ["instructions"]}),
        ("Labels", {'fields': ["labels"]}),
        ("Label Colour", {'fields': ["label_colour"]}),
        ("Slug", {'fields': ["slug"]}),
    ]
    list_display = ('id','title','description','price','labels')

class CartItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order Status", {'fields' : ["status"]}),
        ("Delivery Date", {'fields' : ["delivery_date"]})

    ]
    list_display = ('id','user','item','quantity','ordered','ordered_date','delivery_date','status')
    list_filter = ('ordered','ordered_date','status')

admin.site.register(Item,ItemAdmin)
admin.site.register(CartItems,CartItemsAdmin)
