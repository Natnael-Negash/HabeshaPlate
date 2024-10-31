from django.contrib import admin
from .models import Item, CartItems, Order, Reviews

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Created By", {'fields': ["created_by"]}),
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
    list_display = ('title', 'price', 'pieces', 'created_by', 'created_at')
    list_filter = ('labels', 'created_by')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}  # Automatically generate slug from title
    ordering = ('-created_at',)  # Order items by creation date (newest first)

class CartItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order Status", {'fields': ["status"]}),
        ("Delivery Date", {'fields': ["delivery_date"]}),
    ]
    list_display = ('user', 'item', 'quantity', 'ordered', 'ordered_date', )
    list_filter = ('user', 'ordered')  # Filter options for users and order status
    search_fields = ('item__title',)  # Search items by title

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'ordered_date', 'updated_date')  # Show key order fields
    list_filter = ('status', 'user')  # Filter by order status and user
    search_fields = ('user__username',)  # Search by username

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'review', 'posted_on')  # Display user, item, review, and date posted
    list_filter = ('item',)  # Filter reviews by item
    search_fields = ('review',)  # Search through reviews

# Registering the models with their respective admin classes
admin.site.register(Item, ItemAdmin)
admin.site.register(CartItems, CartItemsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Reviews, ReviewsAdmin)
