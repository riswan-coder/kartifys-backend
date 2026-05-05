from django.db import models
from shops.models import Shop


class Ad(models.Model):
    SLOT_1 = 'slot_1'
    SLOT_2 = 'slot_2'

    SLOT_CHOICES = [
        (SLOT_1, 'Slot 1 — Popup ad (shows on app open)'),
        (SLOT_2, 'Slot 2 — Banner ad (shows in home screen)'),
    ]

    shop = models.ForeignKey(
        Shop,
        on_delete=models.CASCADE,
        related_name='ads'
    )
    slot = models.CharField(
        max_length=10,
        choices=SLOT_CHOICES,
        default=SLOT_1
    )
    image = models.ImageField(
        upload_to='ads/',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_slot_display()} — {self.shop.name}"

    class Meta:
        ordering = ['-created_at']