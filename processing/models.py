from django.db import models
from django.conf import settings
from django.db.models import Sum, F
import datetime

# Create your models here.
User = settings.AUTH_USER_MODEL


class Product(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    # price = models.IntegerField(null=True, blank=False)
    # cost_price = models.IntegerField(null=False, blank=True, default=0)
    # quantity = models.IntegerField(default=0)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

    @property
    def total_stock(self):
        current_stock = ProcessingSale.objects.filter(item=self.id).values('item').annotate(total=Sum('quantity')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_stock_today(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()

        current_stock = ProcessingSale.objects.filter(item=self.id, timestamp__date=d).values('item').annotate(
            total=Sum('quantity')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_sale(self):
        from sales.models import Sale, CreditSale
        current_stock = Sale.objects.filter(item=self.id).values('item').annotate(
            total=Sum('quantity')).values_list('total')
        credit_stock = CreditSale.objects.filter(item=self.id).values('item').annotate(
            total=Sum('quantity')).values_list('total')

        if current_stock:
            if credit_stock:
                return current_stock[0][0] + credit_stock[0][0]
            else:
                return current_stock[0][0]
        elif credit_stock:
            if credit_stock:
                return 0 + credit_stock[0][0]
            else:
                return 0
        else:
            return 0

    @property
    def total_sale_today(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()

        from sales.models import Sale, CreditSale
        current_stock = Sale.objects.filter(item=self.id, timestamp__date=d).values('item').annotate(
            total=Sum('quantity')).values_list('total')
        credit_stock = CreditSale.objects.filter(item=self.id, timestamp__date=d).values('item').annotate(
            total=Sum('quantity')).values_list('total')

        if current_stock:
            if credit_stock:
                return current_stock[0][0] + credit_stock[0][0]
            else:
                return current_stock[0][0]
        elif credit_stock:
            if credit_stock:
                return 0 + credit_stock[0][0]
            else:
                return 0
        else:
            return 0

    @property
    def stock_now(self):
        now_stock = (self.total_stock - self.total_sale)
        return now_stock

    def total_out_t(self):
        t_out = self.total_sale_today
        return t_out

    def asset_value(self):
        percent = self.stock_now
        return percent

    def __str__(self):
        return self.title


class Supply(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL, related_name='item')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    added_date = models.DateTimeField(auto_now_add=True,)

    def current_stock(self):
        return self.item.all().aggregate(models.Sum('quantity'))['quantity__sum']
        # return Inventory.objects.annotate(qty=models.Sum('purchase__quantity'))


class SupplyInvoice(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    description = models.CharField(max_length=255, null=True, blank=True)
    invoice_no = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True,)

    # @property
    # def sum_total(self):
    #     current_stock = SupplySale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
    #         total=Sum(F('price') * F("quantity"))).values_list('total')
    #     if current_stock:
    #         return current_stock[0][0]
    #     else:
    #         return 0


class SupplySale(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    item = models.ForeignKey(Product, null=True, related_name='purchase', on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    # price = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True,)

    @property
    def total_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return self.item


class ProcessingInvoice(models.Model):
    # CASH = 'CS'
    # CHEQUE = 'CQ'
    # SALES_TYPE_CHOICES = [
    #     ('CS', 'Cash'),
    #     ('CQ', 'Cheque'),
    # ]
    item = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    # customer_d = models.ForeignKey('customers.Customer', null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    # sale_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICES,)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def sum_total(self):
        ttl_sale = ProcessingSale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum("quantity")).values_list('total')
        if ttl_sale:
            return ttl_sale[0][0]
        else:
            return 0


class ProcessingSale(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    item = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    # price = models.IntegerField(null=True, blank=True)
    # cost = models.IntegerField(null=True, blank=True, default=0)
    # sale_type = models.CharField(max_length=10, choices=ProcessingInvoice.SALES_TYPE_CHOICES)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True,)

    # @property
    # def total_cost(self):
    #     return self.quantity * self.price

    # @property
    # def cash_bal(self):
    #     return sum(self.total_cost)

    def __str__(self):
        return self.item

