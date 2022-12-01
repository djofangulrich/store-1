import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from store.models import *


class ProductListView(ListView):
    template_name = 'store/product_list.html'
    model = Product
    allow_empty = True
    paginate_by = 12
    paginate_orphans = 0
    context_object_name = "products"
    ordering = None

    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class ProductDetailView(DetailView):
    template_name = 'store/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']

    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
