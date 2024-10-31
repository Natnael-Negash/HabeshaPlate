from django.urls import path
from . import views
from .views import (
    MenuListView,
    menuDetail,
    add_to_cart,
    get_cart_items,
    order_item,
    # CartDeleteView,
    order_details,
    admin_view,
    item_list,
    pending_orders,
    ItemCreateView,
    ItemUpdateView,
    ItemDeleteView,
    update_status,
    add_reviews,
)

app_name = "menu"

urlpatterns = [
    # Menu and Home Views
    path('', MenuListView.as_view(), name='home'),
    path('dishes/<slug>/', menuDetail, name='dishes'),
    
    # Item Management
    path('item_list/', item_list, name='item_list'),
    path('item/new/', ItemCreateView.as_view(), name='item_new'),
    path('item/update/<slug>/', ItemUpdateView.as_view(), name='item_update'),
    path('item/delete/<slug>/', ItemDeleteView.as_view(), name='item_delete'),
    
    # Cart and Orders
    # path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('add-to-cart/<slug:slug>/', views.add_to_cart, name='add-to-cart'),
    path('cart/', get_cart_items, name='cart'),
    # path('cart/delete/<int:pk>/', CartDeleteView.as_view(), name='remove_from_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove-from-cart'),
    path('ordered/', order_item, name='ordered'),
    path('order_details/', order_details, name='order_details'),
    
    # Admin and Order Management
    path('admin_view/', admin_view, name='admin_view'),
    path('pending_orders/', pending_orders, name='pending_orders'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('update_status/<int:pk>/', update_status, name='update_status'),
    
    # Reviews
    path('postReview/', add_reviews, name='add_reviews'),
]
