from django.db import models
from django.conf import settings
from django.db.models import Sum, F

# Create your models here.
User = settings.AUTH_USER_MODEL


class Invoice(models.Model):
    # CASH = 'CS'
    # CREDIT = 'CR'
    # SALES_TYPE_CHOICES = [
    #     ('CS', 'Cash'),
    #     ('CR', 'Credit'),
    # ]
    customer = models.CharField(max_length=255)
    customer_d = models.ForeignKey('customers.Customer', null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    # sale_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICES,)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def sum_total(self):
        current_stock = Sale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum(F('price') * F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0


class Sale(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    item = models.ForeignKey('processing.Product', null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    # sale_type = models.CharField(max_length=10, choices=Invoice.SALES_TYPE_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True,)

    @property
    def total_cost(self):
        return self.quantity * self.price

    @property
    def cash_bal(self):
        return sum(self.total_cost)

    def __str__(self):
        return self.item


class CreditInvoice(models.Model):
    customer = models.ForeignKey('customers.Customer', null=True, on_delete=models.SET_NULL)
    # invoice_no = models.IntegerField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def sum_total(self):
        current_stock = CreditSale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum(F('price') * F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0


class CreditSale(models.Model):
    invoice_no = models.ForeignKey(CreditInvoice, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey('customers.Customer', null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey('processing.Product', null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    # cost = models.IntegerField(null=True, blank=True, default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return self.item
