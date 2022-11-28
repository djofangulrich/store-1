import os

from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from core.settings import AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Categorie"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Marque(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Marque"
        verbose_name_plural = "Marques"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Nom du produit", max_length=255)
    slug = models.SlugField("Slug", max_length=255)
    price = models.IntegerField("Prix", default=0)
    category = models.ForeignKey(Category, verbose_name="Catégorie", on_delete=models.CASCADE, blank=True, null=True)
    tag = models.ManyToManyField(Tag, verbose_name="Tag", related_name="products", blank=True)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField("Quantité en stock", default=0)
    description = RichTextField(verbose_name="Description", blank=True, null=True)

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "produits"

    def __str__(self):
        return f"{self.name} ({self.stock})"

    def get_absolute_url(self):
        return reverse('store:detail', kwargs={"slug": self.slug})

    def get_all_images(self):
        return ProductImage.objects.filter(produit=self)

    def get_first_image(self):
        return ProductImage.objects.filter(produit=self)[0]

    def visuel(self):
        return mark_safe('<img src="{}" alt="{}" width="100" />'.format(self.get_first_image().thumbnail.url, self.name))

    visuel.allow_tags = True


def img_path(instance, filename):
    path = "store/product/"
    ext = filename.split('.')[-1]
    if instance.produit.category:
        path += instance.produit.name + "/"
    return os.path.join(path, filename)


class ProductImage(models.Model):
    produit = models.ForeignKey(Product, related_name='photos', on_delete=models.CASCADE)
    thumbnail = models.ImageField("Photo du produit", upload_to=img_path)

    class Meta:
        verbose_name = "photo de Produit"
        verbose_name_plural = "photos de produit"

    def __str__(self):
        return self.produit.name

    def visuel(self):
        return mark_safe(
            '<img src="{}" alt="{}" width="100" height="100" />'.format(self.thumbnail.url, self.produit.name))

    visuel.allow_tags = True

    @property
    def thumbnailURL(self):
        try:
            url = self.thumbnail.url
        except:
            url = "/static/assets/img/placeholder.png"
        return url


class Customer(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.user.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField("Quantité", default=0, null=True, blank=True)
    date_added = models.DateTimeField("Date d'ajout", auto_now_add=True)

    class Meta:
        verbose_name = "Article commandé"
        verbose_name_plural = "Articles commandés"

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField("Adresse", max_length=200, null=False)
    city = models.CharField("Ville", max_length=200, null=False)
    state = models.CharField("Pays", max_length=200, null=False)
    zipcode = models.CharField("Code postal", max_length=200, null=False)
    date_added = models.DateTimeField("Date d'ajout", auto_now_add=True)

    class Meta:
        verbose_name = "Adresse de livraison"
        verbose_name_plural = "Adresses de livraison"

    def __str__(self):
        return self.address
