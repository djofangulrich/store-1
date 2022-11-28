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
