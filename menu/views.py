from django.shortcuts import render, get_object_or_404, redirect

from .decorators import admin_required
from .models import Item, CartItems, Reviews, Order
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse

class MenuListView(ListView):
    model = Item
    template_name = 'menu/home.html'
    context_object_name = 'menu_items'

def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    context = {
        'item' : item,
        'reviews' : reviews,
    }
    return render(request, 'menu/dishes.html', context)

@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    return redirect(f"/dishes/{item.slug}")

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.created_by

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/item_list'

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.created_by
@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(CartItems, id=cart_id)
    cart_item.delete()  # Remove the item from the cart
    return redirect('menu:cart')
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        ordered=False,
    )
    messages.info(request, "Added to Cart!! Continue Shopping!!")
    return redirect("menu:cart")

@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    bill = cart_items.aggregate(Sum('item__price'))
    number = cart_items.aggregate(Sum('quantity'))
    pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum") or 0
    count = number.get("quantity__sum") or 0
    total_pieces = pieces.get("item__pieces__sum") or 0
    context = {
        'cart_items': cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'menu/cart.html', context)

"""class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        return self.request.user == cart.user"""

@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user, ordered=False)
    if cart_items.exists():
        ordered_date = timezone.now()
        
        # Create a new Order instance
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        for item in cart_items:
            item.ordered = True
            item.ordered_date = ordered_date
            item.save()
            order.cart_items.add(item)  # Link cart item to order

        order.save()  # Save the order instance
        messages.info(request, "Item Ordered")
    else:
        messages.warning(request, "Your cart is empty.")
    
    return redirect("menu:order_details")

@login_required
def order_details(request):
    orders = Order.objects.filter(user=request.user).order_by('-ordered_date')
    context = {
        'orders': orders,
    }
    return render(request, 'menu/order_details.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True, status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items': cart_items,
    }
    return render(request, 'menu/admin_view.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def item_list(request):
    items = Item.objects.filter(created_by=request.user)
    context = {
        'items': items
    }
    return render(request, 'menu/item_list.html', context)

@login_required
@admin_required
def update_status(request, pk):
    if request.method == 'POST':
        status = request.POST['status']
        cart_items = CartItems.objects.filter(item__created_by=request.user, ordered=True, status="Active", pk=pk)
        delivery_date = timezone.now()
        if status == 'Delivered':
            cart_items.update(status=status, delivery_date=delivery_date)
    return redirect("menu:pending_orders")

@login_required(login_url='/accounts/login/')
@admin_required
def pending_orders(request):
    pending_orders = Order.objects.filter(cart_items__item__created_by=request.user, status="Pending").order_by('-ordered_date')
    context = {
        'orders': pending_orders,
    }
    return render(request, 'menu/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_dashboard(request):
    orders = Order.objects.filter(cart_items__item__created_by=request.user)
    pending_total = orders.filter(status="Pending").count()
    completed_total = orders.filter(status="Delivered").count()
    total_income = orders.aggregate(Sum('cart_items__item__price'))['cart_items__item__price__sum'] or 0

    context = {
        'pending_total': pending_total,
        'completed_total': completed_total,
        'income': total_income,
    }
    return render(request, 'menu/admin_dashboard.html', context)
