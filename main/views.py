from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, CartItems
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from .decorators import *
from django.db.models import Sum

class MenuListView(ListView):
    model = Item
    template_name = 'main/home.html'
    context_object_name = 'menu_items'

class MenuDetailView(DetailView):
    model = Item
    template_name = 'main/dishes.html'

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        ordered=False,
    )
    messages.info(request, "Added to Cart!!Continue Shopping!!")
    return redirect("main:cart")

@login_required
def get_cart_items(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    total = 0
    count = 0
    total_pieces = 0
    for cart_item in cart_items:
        total += float(cart_item.item.price)
        count += int(cart_item.quantity)
        total_pieces += int(cart_item.item.pieces)
    context = {
        'cart_items':cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'main/cart.html', context)

class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False

@login_required
def order_item(request):
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    ordered_date=timezone.now()
    cart_items.update(ordered=True,ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("main:order_details")

@login_required
def order_details(request):
    items = CartItems.objects.filter(ordered=True,status="Active").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(ordered=True,status="Delivered").order_by('-ordered_date')
    total = 0
    count = 0
    total_pieces = 0
    for item_active in items:
        total += float(item_active.item.price)
        count += int(item_active.quantity)
        total_pieces += int(item_active.item.pieces)
    context = {
        'items':items,
        'cart_items':cart_items,
        'total': total,
        'count': count,
        'total_pieces': total_pieces
    }
    return render(request, 'main/order_details.html', context)


@login_required(login_url='/accounts/login/')
@admin_required
def admin_view(request):
    cart_items = CartItems.objects.filter(ordered=True,status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def pending_orders(request):
    items = CartItems.objects.filter(ordered=True,status="Active").order_by('-ordered_date')
    context = {
        'items':items,
    }
    return render(request, 'main/pending_orders.html', context)

@login_required(login_url='/accounts/login/')
@admin_required
def admin_dashboard(request):
    cart_items = CartItems.objects.all()
    pending_total = CartItems.objects.filter(ordered=True,status="Active").count()
    completed_total = CartItems.objects.filter(ordered=True,status="Delivered").count()
    count1 = CartItems.objects.filter(ordered=True,item="1").count()
    count2 = CartItems.objects.filter(ordered=True,item="2").count()
    total = 0
    for item_active in cart_items:
        total += float(item_active.item.price)
    context = {
        'pending_total' : pending_total,
        'completed_total' : completed_total,
        'total' : total,
        'count1' : count1,
        'count2' : count2,
    }
    print(context)
    return render(request, 'main/admin_dashboard.html', context)

