from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime
import csv
import xlwt
from django.http import HttpResponse
from _datetime import date

# Create your views here.
from .forms import (
    InventoryForm,
    PurchaseForm,
    PurchaseInvoiceForm,
    # SalesReturnForm,
    ProcessingForm,
    ProcessSaleForm,
)
from django.core.paginator import Paginator
from django.db.models import Sum
from .filters import *


@login_required
def processing_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = ProcessingForm(request.POST or None)
    # form1 = RegInvoiceForm(request.POST or None)
    form_head = 'Processing Invoice'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        count = ProcessingInvoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.user = request.user
        obj.save()
        form = ProcessingForm()
        lst = ProcessingInvoice.objects.latest('invoice_no')
        request.session['invoice'] = lst.invoice_no
        # request.session['sale_type'] = lst.sale_type
        return redirect('/process_invoice')

    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = ProcessingInvoice.objects.filter().order_by('-timestamp')
        else:
            qs = ProcessingInvoice.objects.filter(timestamp__date=date.today().strftime('%Y-%m-%d')).order_by('-timestamp')
    else:
        qs = ProcessingInvoice.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-timestamp')
    my_filter = InvoiceFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # page_obj = qs
    return render(request, "process_sale.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def processing_edit_view(request, pk):
    obj = get_object_or_404(ProcessingInvoice, id=pk)
    form = ProcessingForm(instance=obj)
    form_head = 'Processing Invoice'
    if request.method == 'POST':
        form = ProcessingForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            # qs1 = ProcessSupply.objects.get(id=pk)
            # invc = request.session.get('invoice')
            form = ProcessingForm()
            return redirect('/processing')
    qs = ProcessingInvoice.objects.filter().order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = ""

    return render(request, "process_sale.html", {"form": form, "edit": 'edit', "form_head": form_head, "object": page_obj})


@login_required
def process_sales_view(request):
    form = ProcessSaleForm(request.POST or None)
    form_head = 'Processed Material'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = request.session.get('invoice')
        # obj.sale_type = request.session.get('sale_type')
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        # obj.cost = form.instance.item.cost_price
        obj.user = request.user
        obj.save()
        form = ProcessSaleForm()
        return redirect('/process_invoice')
    qs = ProcessingSale.objects.filter(invoice_no=request.session.get('invoice')).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session['invoice'], '06')
    obj1 = ProcessingInvoice.objects.filter(id=inv)
    # total_price = Sale.objects.all().annotate(total=Sum('price'))
    # total_price1 = Sale.objects.filter(invoice_no=request.session.get('invoice')).aggregate(Sum('total_cost'))
    obj2 = obj1[0]
    return render(request, "process_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def process_view_sales(request, inv=None, *args, **kwargs):
    form = ProcessSaleForm(request.POST or None)
    form_head = 'Processing Invoice'
    st = ProcessingInvoice.objects.get(invoice_no=inv)
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = inv
        # obj.sale_type = st
        # if not form.data['price']:
        #     obj.price = form.instance.item.price
        # else:
        #     obj.price = form.data['price']
        obj.user = request.user
        obj.save()
        form = ProcessSaleForm()
        request.session['invoice'] = inv
        # request.session['sale_type'] = st
        return redirect('/process_invoice')
    qs = ProcessingSale.objects.filter(invoice_no=inv).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = ProcessingInvoice.objects.filter(id=inv)
    # total_price = ProcessingSale.objects.all().annotate(total=Sum('price'))
    obj2 = obj1[0]
    return render(request, "process_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def process_sales_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(ProcessingSale, id=pk)
    form = ProcessSaleForm(instance=obj)
    form_head = 'Sales Invoice'
    # print(form.errors)
    if request.method == 'POST':
        form = ProcessSaleForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # if not form.data['price']:
            #     obj.price = form.instance.item.price
            # else:
            #     obj.price = form.data['price']
            obj.save()
            qs1 = ProcessingSale.objects.get(id=pk)
            # invc = request.session.get('invoice')
            request.session['invoice'] = qs1.invoice_no
            return redirect('/process_invoice')
    qs = ProcessingSale.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    qs = ProcessingSale.objects.get(id=pk)
    inv = format(qs.invoice_no, '06')
    obj1 = ProcessingInvoice.objects.filter(id=inv)
    obj2 = obj1[0]
    return render(request, "process_invoice.html", {"form": form, "form_head": form_head, "object": '', "object1": obj2})


@login_required
def process_sales_delete_view(request, pk):
    qs1 = ProcessingSale.objects.get(id=pk)
    request.session['invoice'] = qs1.invoice_no
    obj = get_object_or_404(ProcessingSale, id=pk)
    obj.delete()
    return redirect('/process_invoice')


@login_required
def product_view(request):
    form = InventoryForm(request.POST or None)
    form_head = 'Products'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = InventoryForm()
    qs = Product.objects.filter().order_by('title')
    my_filter = InventoryFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "products.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def product_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Product, id=pk)
    form = InventoryForm(instance=obj)
    form_head = 'Products'
    # print(form.errors)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/products')
    qs = Product.objects.filter(id=pk).order_by('title')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    page_obj = ""
    return render(request, "products.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def product_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Product, id=pk)
    obj.delete()
    return redirect('/products')


@login_required
def supply_invoice_view(request):
    form = PurchaseInvoiceForm(request.POST or None)
    form_head = 'Purchase'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        count = SupplyInvoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.user = request.user
        obj.save()
        lst = SupplyInvoice.objects.latest('id')
        request.session['invoice'] = lst.id
        form = PurchaseInvoiceForm()
        return redirect('/purchase_invoice')
        # Inventory.objects.filter(id=).update(field1=2)
    qs = SupplyInvoice.objects.filter().order_by('-added_date')
    my_filter = PurchaseFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "purchase.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def view_supply_invoice(request, inv=None, *args, **kwargs):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchased Goods'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = inv
        obj.user = request.user
        obj.save()
        form = PurchaseForm()
        request.session['invoice'] = inv
        return redirect('/purchase_invoice')
    qs = SupplySale.objects.filter(invoice_no=inv).order_by('-timestamp')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = SupplyInvoice.objects.filter(id=inv)
    total_price = SupplySale.objects.all().annotate(total=Sum('price'))
    obj2 = obj1[0]
    return render(request, "purchase_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def supply_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(SupplySale, id=pk)
    form = PurchaseForm(instance=obj)
    form_head = 'Purchased Goods'
    # print(form.errors)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.price = form.instance.item.price
            obj.save()
            qs1 = SupplySale.objects.get(id=pk)
            request.session['invoice'] = qs1.invoice_no
            return redirect('/purchase_invoice')
    qs = SupplySale.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session.get('invoice'), '06')
    obj1 = SupplyInvoice.objects.filter(id=inv)
    obj2 = obj1
    return render(request, "invoice.html", {"form": form, "form_head": form_head, "object": page_obj, "object1": obj2})


@login_required
def supply_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    qs1 = SupplySale.objects.get(id=pk)
    request.session['invoice'] = qs1.invoice_no
    obj = get_object_or_404(SupplySale, id=pk)
    obj.delete()
    return redirect('/purchase_invoice')


@login_required
def supply_sales_view(request):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchased Goods'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = request.session.get('invoice')
        # obj.price = form.instance.item.price
        obj.user = request.user
        obj.save()
        form = PurchaseForm()
        return redirect('/purchase_invoice')
    qs = SupplySale.objects.filter(invoice_no=request.session.get('invoice')).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session['invoice'], '06')
    obj1 = SupplyInvoice.objects.filter(id=inv)
    total_price = SupplySale.objects.all().annotate(total=Sum('price'))
    obj2 = obj1
    return render(request, "purchase_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2})


@login_required
def supply_view(request):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchase'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = PurchaseForm()
        # Inventory.objects.filter(id=).update(field1=2)
    qs = Supply.objects.filter().order_by('-added_date')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "purchase.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def stock_report_view(request):
    qs = Product.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    # qs = my_filter.qs
    paginator = Paginator(qs, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "stock_report.html", {"object": page_obj, "myFilter": my_filter})


def export_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Stock Report' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'sale Price', 'Opening Stock', 'Inflow', 'Sales', 'closing Stock'])

    qs = Product.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    for row_data in qs:
        writer.writerow([row_data.title, row_data.price, row_data.stock_now, row_data.total_stock, row_data.total_sale, row_data.stock_now])

    return response


def export_excel_view(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['content-disposition'] = 'attachment; filename=KDV Stock Report' + str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Stock Report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'sale Price', 'Opening Stock', 'Inflow', 'Sales', 'closing Stock']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    qs = Product.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    # rows = my_filter.qs.values_list()
    rows = my_filter.qs

    for row in rows:
        row_num = 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)

    return response


def export_csv_stock(request):
    now = datetime.datetime.now()
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            ddate = request.GET.get('timestamp')
        else:
            ddate = now
    else:
        ddate = now
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Stock Valuation as at ' + str(ddate)+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Opening Stock', 'Inflow', 'Sales', 'closing Stock', 'Avg Cost', 'Asset Value', '% of Tot Asset', 'Sale Price', 'Retail Value', '% of Tot Retail'])

    # qs = Inventory.objects.filter().order_by('title')
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            sdate = request.GET.get('timestamp')
        else:
            sdate = now
        qs = Product.objects.filter().order_by('title')
    else:
        qs = Product.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    qs = my_filter.qs

    grand_total = 0
    tt_inflow = 0
    tt_sale = 0
    tt_cl = 0
    tt_asset = 0
    tt_retail = 0
    r_tt = 0
    a_tt = 0
    for rw in qs:
        r_t = rw.price * rw.stock_now
        a_t = rw.cost_price * rw.stock_now
        r_tt += r_t
        a_tt += a_t
    for row_data in qs:
        r_open = row_data.stock_now + row_data.total_sale_today + row_data.total_promo_today + row_data.total_damages_today + row_data.total_return_o
        asset_value = row_data.cost_price * row_data.stock_now
        retail_value = row_data.price * row_data.stock_now
        perc = retail_value / r_tt * 100
        a_perc = asset_value / a_tt * 100

        writer.writerow([row_data.title, r_open, row_data.total_stock_today, row_data.total_sale_today, f"{row_data.stock_now:,.2f}", f"{row_data.cost_price:,.2f}", f"{asset_value:,.2f}", f"{a_perc:,.2f} %", f"{row_data.price:,.2f}", f"{retail_value:,.2f}", f"{perc:,.2f} %"])
        grand_total += r_open
        tt_inflow += row_data.total_stock_today
        tt_sale += row_data.total_sale_today
        tt_cl += row_data.stock_now
        tt_asset += asset_value
        tt_retail += retail_value
    writer.writerow(['Total', f"{grand_total:,.2f}", tt_inflow, tt_sale, f"{tt_cl:,.2f}", '', f"{tt_asset:,.2f}", '100.0%', '', f"{tt_retail:,.2f}", '100.0%'])

    return response


# @login_required
# def report_view(request):
#     oqs = Sale.objects.filter(sale_type='CS').annotate(
#         total_cost=ExpressionWrapper(
#             F('price') * F('quantity'),
#             output_field=DecimalField()
#         )
#     ).aggregate(sum_total=Sum('total_cost'))['sum_total']
