from django.db import models
from shops.models import Shop

class Category(models.Model):
    # Gender category
    MEN = 'men'
    WOMEN = 'women'
    KIDS = 'kids'

    GENDER_CHOICES = [
        (MEN, 'Men'),
        (WOMEN, 'Women'),
        (KIDS, 'Kids'),
    ]

    # Product type
    CLOTHES = 'clothes'
    SHOES = 'shoes'

    TYPE_CHOICES = [
        (CLOTHES, 'Clothes'),
        (SHOES, 'Shoes'),
    ]

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    product_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.get_gender_display()} - {self.get_product_type_display()}"

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['gender', 'product_type']


class Product(models.Model):
    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sizes = models.CharField(
        max_length=100,
        blank=True,
        help_text='e.g. S,M,L,XL or 6,7,8,9,10'
    )
    colors = models.CharField(
        max_length=100,
        blank=True,
        help_text='e.g. Red,Blue,Black'
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.shop.name}"

    class Meta:
        ordering = ['-created_at']

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='products/',
        blank=False,
        null=False
    )
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"