from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

import csv
import xlwt
from django.http import HttpResponse
from _datetime import date


# Create your views here.
from .forms import (
    ExpensesForm,
    InventoryForm,
    PurchaseForm,
    SupplyForm,
    RegInvoiceForm,
    PurchaseInvoiceForm,
)
from django.core.paginator import Paginator
from django.db.models import Sum
from .filters import *


@login_required
def expenses_view(request, month=None):
    from datetime import datetime
    if month is None:
        month = datetime.today().month
        year = datetime.today().year
    form = ExpensesForm(request.POST or None)
    form_head = 'Daily Expenses'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = ExpensesForm()

    if request.GET.get('timestamp'):
        if request.GET.get('added_date') != '':
            qs = Expenses.objects.filter().order_by('-id')
        else:
            qs = Expenses.objects.filter(added_date__month=month, added_date__year=year).order_by('-id')
    else:
        qs = Expenses.objects.filter(added_date__month=month, added_date__year=year).order_by('-id')
    my_filter = ExpensesFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "page.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def expenses_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Expenses, id=pk)
    form = ExpensesForm(instance=obj)
    form_head = 'Daily Expenses'
    # print(form.errors)
    if request.method == 'POST':
        form = ExpensesForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/expenses')
    qs = Expenses.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "page.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def expenses_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Expenses, id=pk)
    obj.delete()
    return redirect('/expenses')


@login_required
def inventory_view(request):
    form = InventoryForm(request.POST or None)
    form_head = 'Inventory'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = InventoryForm()
    qs = Inventory.objects.filter().order_by('title')
    my_filter = InventoryFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "inventory.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def inventory_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Inventory, id=pk)
    form = InventoryForm(instance=obj)
    form_head = 'Inventory'
    # print(form.errors)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('/inventory')
    qs = Inventory.objects.filter(id=pk).order_by('title')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "inventory.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def inventory_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(Inventory, id=pk)
    obj.delete()
    return redirect('/inventory')


@login_required
def purchase_invoice_view(request, month=None):
    import calendar
    from datetime import datetime
    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = PurchaseInvoiceForm(request.POST or None)
    form1 = RegInvoiceForm(request.POST or None)
    form_head = 'Purchase'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        count = PurchaseInvoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.sale_type = 'CS'
        obj.user = request.user
        obj.save()
        lst = PurchaseInvoice.objects.latest('id')
        request.session['invoice'] = lst.id
        request.session['sale_type'] = lst.sale_type
        request.session['supplier'] = lst.supplier_d_id
        form = PurchaseInvoiceForm()
        return redirect('/purchase_invoice')
        # Inventory.objects.filter(id=).update(field1=2)
    elif form1.is_valid():
        cd = form1.cleaned_data
        obj = form1.save(commit=False)
        count = PurchaseInvoice.objects.all().count()
        obj.invoice_no = count + 1
        obj.description = form1.instance.supplier_d.name
        obj.user = request.user
        obj.save()
        lst = PurchaseInvoice.objects.latest('id')
        request.session['invoice'] = lst.id
        request.session['sale_type'] = lst.sale_type
        request.session['supplier'] = lst.supplier_d_id
        form = PurchaseInvoiceForm()
        return redirect('/purchase_invoice')
        # Inventory.objects.filter(id=).update(field1=2)
    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = PurchaseInvoice.objects.filter().order_by('-added_date')
        else:
            qs = PurchaseInvoice.objects.filter(added_date__date=date.today().strftime('%Y-%m-%d')).order_by('-added_date')
    else:
        qs = PurchaseInvoice.objects.filter(added_date__month=month, added_date__year=year).order_by('-added_date')

    # qs = PurchaseInvoice.objects.filter().order_by('-added_date')
    my_filter = PurchaseFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "new_purchase.html", {"form": form, "form1": form1, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def view_purchase_invoice(request, inv=None, *args, **kwargs):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchase Invoice'
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
    qs = PurchaseSale.objects.filter(invoice_no=inv).order_by('-timestamp')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(inv, '06')
    obj1 = PurchaseInvoice.objects.filter(id=inv)
    total_price = PurchaseSale.objects.all().annotate(total=Sum('price'))
    for rw in obj1:
        cust = rw.supplier_d_id
        qs1 = Suppliers.objects.filter(id=cust)
    obj2 = obj1[0]
    print(obj2)
    return render(request, "purchase_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2, "object2": qs1})


@login_required
def purchase_edit_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(PurchaseSale, id=pk)
    form = PurchaseForm(instance=obj)
    form_head = 'Edit Purchased Goods'
    qs1 = PurchaseSale.objects.get(id=pk)
    request.session['invoice'] = qs1.invoice_no
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            # obj.price = form.instance.item.price
            obj.save()

            return redirect('/purchase_invoice')
    print(pk)
    qs = PurchaseSale.objects.filter(id=pk).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session.get('invoice'), '06')
    obj1 = PurchaseInvoice.objects.filter(id=inv)
    obj2 = obj1
    return render(request, "purchase_invoice.html", {"form": form, "form_head": form_head, "object": '', "object1": obj2})


@login_required
def purchase_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    qs1 = PurchaseSale.objects.get(id=pk)
    request.session['invoice'] = qs1.invoice_no
    obj = get_object_or_404(PurchaseSale, id=pk)
    obj.delete()
    return redirect('/purchase_invoice')


@login_required
def purchase_sales_view(request):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchase Invoice'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = request.session.get('invoice')
        obj.sale_type = request.session.get('sale_type')
        obj.supplier_d = request.session.get('supplier')
        # obj.price = form.instance.item.price
        obj.user = request.user
        obj.save()
        form = PurchaseForm()
        return redirect('/purchase_invoice')
    qs = PurchaseSale.objects.filter(invoice_no=request.session.get('invoice')).order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    inv = format(request.session['invoice'], '06')
    obj1 = PurchaseInvoice.objects.filter(id=inv)
    total_price = PurchaseSale.objects.all().annotate(total=Sum('price'))
    for rw in obj1:
        cust = rw.supplier_d_id
        qs1 = Suppliers.objects.filter(id=cust)
    obj2 = obj1[0]
    print(obj2)
    return render(request, "purchase_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, 'invoice': inv, "object1": obj2, "object2": qs1})


@login_required
def purchase_view(request):
    form = PurchaseForm(request.POST or None)
    form_head = 'Purchase'
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        form = PurchaseForm()
        # Inventory.objects.filter(id=).update(field1=2)
    qs = Purchase.objects.filter().order_by('-added_date')
    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "purchase.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def supply_view(request, month=None):
    from datetime import datetime

    if month is None:
        month = datetime.today().month
        year = datetime.today().year

    form = SupplyForm(request.POST or None)
    form_head = 'Transfers'
    # print(form.errors)
    if form.is_valid():
        cd = form.cleaned_data
        obj = form.save(commit=False)
        obj.invoice_no = request.session.get('invoice')
        obj.sale_type = request.session.get('sale_type')

        # obj.cost = form.instance.item.cost_price
        obj.user = request.user
        obj.save()
        form = SupplyForm()
        return redirect('/transfer')

    if request.GET.get('timestamp'):
        if request.GET.get('timestamp') != '':
            qs = ProcessSupply.objects.filter().order_by('-id')
        else:
            qs = ProcessSupply.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-id')
    else:
        qs = ProcessSupply.objects.filter(timestamp__month=month, timestamp__year=year).order_by('-id')
    my_filter = SupplyFilter(request.GET, queryset=qs)
    qs = my_filter.qs
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # inv = format(request.session['invoice'], '06')
    # obj1 = Invoice.objects.filter(id=inv)
    # total_price = Sale.objects.all().annotate(total=Sum('price'))
    # total_price1 = Sale.objects.filter(invoice_no=request.session.get('invoice')).aggregate(Sum('total_cost'))
    # obj2 = obj1[0]
    return render(request, "supply_invoice.html", {"form": form, "form_head": form_head, "object": page_obj, "myFilter": my_filter})


@login_required
def supply_edit_view(request, pk):
    obj = get_object_or_404(ProcessSupply, id=pk)
    form = SupplyForm(instance=obj)
    form_head = 'Transfers'
    if request.method == 'POST':
        form = SupplyForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            # qs1 = ProcessSupply.objects.get(id=pk)
            # invc = request.session.get('invoice')
            form = SupplyForm()
            return redirect('/transfer')
    qs = ProcessSupply.objects.filter().order_by('-id')
    paginator = Paginator(qs, 100)
    page_number = request.GET.get('page')
    page_obj = ""

    return render(request, "supply_invoice.html", {"form": form, "form_head": form_head, "object": page_obj})


@login_required
def supply_delete_view(request, pk):
    # obj = Expenses.objects.get(id=pk)
    obj = get_object_or_404(ProcessSupply, id=pk)
    obj.delete()
    return redirect('/transfer')


@login_required
def stock_report_view(request):
    qs = Inventory.objects.filter().order_by('title')
    my_filter = ReportFilter(request.GET, queryset=qs)
    # qs = my_filter.qs
    paginator = Paginator(qs, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "stock_report.html", {"object": page_obj, "myFilter": my_filter})


@login_required
def raw_report_view(request):
    qs = Product.objects.filter().order_by('title')
    my_filter = RawReportFilter(request.GET, queryset=qs)
    # qs = my_filter.qs
    paginator = Paginator(qs, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "finished_report.html", {"object": page_obj, "myFilter": my_filter})


def export_csv_view(request):
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=KDV Stock Report' + str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Name', 'sale Price', 'Opening Stock', 'Inflow', 'Sales', 'closing Stock'])

    qs = Inventory.objects.filter().order_by('title')
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

    qs = Inventory.objects.filter().order_by('title')
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
        qs = Inventory.objects.filter().order_by('title')
    else:
        qs = Inventory.objects.filter().order_by('title')
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
