from django.db import models
from accounts.models import User


class Shop(models.Model):
    MEN_CLOTHES = 'men_clothes'
    MEN_SHOES = 'men_shoes'
    WOMEN_CLOTHES = 'women_clothes'
    WOMEN_SHOES = 'women_shoes'
    KIDS_CLOTHES = 'kids_clothes'
    KIDS_SHOES = 'kids_shoes'

    CATEGORY_CHOICES = [
        (MEN_CLOTHES, 'Men Clothes'),
        (MEN_SHOES, 'Men Shoes'),
        (WOMEN_CLOTHES, 'Women Clothes'),
        (WOMEN_SHOES, 'Women Shoes'),
        (KIDS_CLOTHES, 'Kids Clothes'),
        (KIDS_SHOES, 'Kids Shoes'),
    ]

    owner = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='shop',
        limit_choices_to={'role': 'shop_owner'},
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    logo = models.ImageField(
        upload_to='shop_logos/',
        blank=True,
        null=True
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=MEN_CLOTHES
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
       ordering = ['created_at']  # oldest first — remove the minus sign