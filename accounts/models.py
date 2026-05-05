from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Three roles in EasyFind
    CUSTOMER = 'customer'
    SHOP_OWNER = 'shop_owner'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SHOP_OWNER, 'Shop Owner'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=CUSTOMER
    )
    phone = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

    # Helper properties — easy to check role anywhere in code
    @property
    def is_customer(self):
        return self.role == self.CUSTOMER

    @property
    def is_shop_owner(self):
        return self.role == self.SHOP_OWNER

    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
import random
from django.utils import timezone


class OTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='otps'
    )
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # OTP valid for 10 minutes
        expiry = self.created_at + timezone.timedelta(minutes=10)
        return not self.is_used and timezone.now() < expiry

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"OTP for {self.user.username} — {self.code}"