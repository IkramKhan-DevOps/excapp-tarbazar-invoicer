import uuid
from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, help_text="")
    rate = models.FloatField()
    vat = models.FloatField()

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=1000, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    total = models.FloatField(default=00)
    vat = models.FloatField(default=00)
    grand_total = models.FloatField(default=00)

    qr_image = models.ImageField(
        upload_to='accounts/images/wallets/', null=True, blank=True,
        help_text='size of logo must be 200*200 and format must be png image file',
    )
    product_items = models.ManyToManyField(Product, through='InvoiceItem')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(null=False, blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.customer_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_on = timezone.now()
        super(Invoice, self).save(*args, **kwargs)


class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoices')
    quantity = models.PositiveIntegerField(default=1)
    amount = models.FloatField(default=0)
    vat = models.FloatField(default=0)

    class Meta:
        ordering = ['-invoice']

    def __str__(self):
        return self.invoice.customer_name

    def net_total(self):
        total = self.quantity * self.amount
        return total + (total * (self.vat/100))
