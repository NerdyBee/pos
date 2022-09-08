from django.db import models
from django.conf import settings
from django.db.models import Sum, F
import datetime

# Create your models here.
User = settings.AUTH_USER_MODEL


class Inventory(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField(auto_now_add=True,)

    @property
    def total_stock(self):
        current_stock = PurchaseSale.objects.filter(item=self.id).values('item').annotate(total=Sum('quantity')).values_list('total')
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

        current_stock = PurchaseSale.objects.filter(item=self.id, timestamp__date=d).values('item').annotate(
            total=Sum('quantity')).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_sale(self):

        current_stock = ProcessSupply.objects.filter(item=self.id).values('item').annotate(
            total=Sum('quantity')).values_list('total')

        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_sale_today(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()

        current_stock = ProcessSupply.objects.filter(item=self.id, timestamp__date=d).values('item').annotate(
            total=Sum('quantity')).values_list('total')

        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    @property
    def total_buy_today(self, timestamp=None):
        if timestamp:
            d = datetime.datetime.strptime(timestamp, '%d-%m-%Y').strftime('%Y-%m-%d')
        else:
            d = datetime.datetime.now().date()

        current_stock = PurchaseSale.objects.filter(item=self.id, timestamp__date=d).values('item', 'invoice_no').annotate(
            total=Sum('quantity'), cost=Sum(F('price') * F("quantity"))).values_list('total', 'cost')

        print(current_stock)

        if current_stock:
            ttl_ind = 0
            t_cost = 0
            for indv in current_stock:
                ttl_ind += indv[0]
                t_cost += indv[1]
            return [ttl_ind, t_cost]
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


class Expenses(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    added_date = models.DateTimeField(auto_now_add=True,)


class Purchase(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Inventory, null=True, on_delete=models.SET_NULL, related_name='item')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    added_date = models.DateTimeField(auto_now_add=True,)

    def current_stock(self):
        return self.item.all().aggregate(models.Sum('quantity'))['quantity__sum']
        # return Inventory.objects.annotate(qty=models.Sum('purchase__quantity'))


class PurchaseInvoice(models.Model):
    TRANSFER = 'TR'
    CREDIT = 'CR'
    SALES_TYPE_CHOICES = [
        ('TR', 'Transfer'),
        ('CR', 'Credit'),
    ]
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sale_type = models.CharField(max_length=10, default="CS", choices=SALES_TYPE_CHOICES, )
    description = models.CharField(max_length=255, null=True, blank=True)
    supplier_d = models.ForeignKey('suppliers.Suppliers', null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True,)

    @property
    def sum_total(self):
        current_stock = PurchaseSale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum(F('price') * F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0

    def sum_qty(self):
        current_stock = PurchaseSale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum("quantity")).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0


class PurchaseSale(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    item = models.ForeignKey(Inventory, null=True, related_name='purchase', on_delete=models.SET_NULL)
    # supplier_d = models.ForeignKey('suppliers.Suppliers', null=True, on_delete=models.SET_NULL)
    supplier_d = models.IntegerField(null=True)
    sale_type = models.CharField(max_length=10, default="CS", choices=PurchaseInvoice.SALES_TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True,)

    @property
    def total_cost(self):
        return self.quantity * self.price

    def __str__(self):
        return self.item


class ProcessSupply(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    # invoice_no = models.IntegerField()
    item = models.ForeignKey('shop.Inventory', null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return self.item


class SupplierInvoice(models.Model):
    TRANSFER = 'TR'
    CREDIT = 'CR'
    SALES_TYPE_CHOICES = [
        ('TR', 'Transfer'),
        ('CR', 'Credit'),
    ]
    supplier = models.CharField(max_length=255)
    supplier_d = models.ForeignKey('suppliers.Suppliers', null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    sale_type = models.CharField(max_length=10, choices=SALES_TYPE_CHOICES,)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def sum_total(self):
        current_stock = SupplierSale.objects.filter(invoice_no=self.id).values('invoice_no').annotate(
            total=Sum(F('price') * F("quantity"))).values_list('total')
        if current_stock:
            return current_stock[0][0]
        else:
            return 0


class SupplierSale(models.Model):
    # invoice_no = models.ForeignKey(Invoice, null=True, on_delete=models.SET_NULL)
    invoice_no = models.IntegerField()
    item = models.ForeignKey('Inventory', null=True, on_delete=models.SET_NULL)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    sale_type = models.CharField(max_length=10, choices=SupplierInvoice.SALES_TYPE_CHOICES)
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

