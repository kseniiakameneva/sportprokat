# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.db import connection
from prokat.models import Category, Product, Type, Order
from .forms import BookingForm, CheckForm
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import redirect


def base_view(request):
    categories = Category.objects.raw('SELECT * FROM prokat_category ')
    products = Product.objects.raw('SELECT * FROM prokat_product ')
    types = Type.objects.raw('SELECT * FROM prokat_type ')
    context = {
        'categories': categories,
        'products': products,
        'types': types
    }
    return render(request, 'base.html', context)


def prod_list(request, pk):
    # products = Product.objects.filter(category=pk, available=True)
    products = Product.objects.raw(
        "SELECT * FROM prokat_product WHERE (prokat_product.available = 1 AND prokat_product.category_id = %s)", (pk))
    # print(products.query)
    categories = Category.objects.raw('SELECT * FROM prokat_category ')
    context = {
        'categories': categories,
        'products': products,

    }
    return render(request, 'category.html', context)


def rules_view(request):
    return render(request, 'rules.html')


def contact_view(request):
    return render(request, 'contacts.html')


def thankyou_view(request):
    return render(request, 'thankyou.html')


def prod_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'prod_detail.html', {'product': product})


def booking_view(request):
    form = BookingForm(request.POST or None)
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            date1 = product.date
            date2 = product.date_end
            delta = date2 - date1
            check = datetime.now().date()
            if (delta.days >= 0) & (date1 >= check) & (date2 >= check):
                id_pr = Product.objects.filter(title__contains=product.product)
                '''''''''''
                res = Order.objects.raw(
                    'SELECT * FROM prokat_order WHERE prokat_order.product_id = %s '
                    ' AND (prokat_order.date BETWEEN %s AND %s)'
                    ' OR (prokat_order.date_end BETWEEN %s AND %s)  ', (id_pr, product.date,
                                                                        product.date_end, product.date,
                                                                        product.date_end))

                #if HttpResponse(len(list(res))==0:
                for r in res:
                    print(res.title)
                '''''
                res = Order.objects.filter(Q(product=id_pr, date__range=(date1, date2)) | Q(product=id_pr,
                                                                                            date_end__range=(
                                                                                                date1, date2)))
                if res.count() == 0:
                    product.save()
                    return render(request, 'thankyou.html')
                else:
                    return render(request, 'booking.html', {'form': form, 'text': 'На заданные даты товар недоступен!'})
            else:
                return render(request, 'booking.html', {'form': form, 'text': 'Заполните форму корректно!'})

    else:
        form = BookingForm()
        return render(request, 'booking.html', {'form': form})


def get_queryset(request):
    # Получаем не отфильтрованный кверисет всех моделей
    queryset = Product.objects.all()
    q = request.GET.get("q")

    if q != "":
        # Если 'q' в GET запросе, фильтруем кверисет по данным из 'q'
        # products = queryset.filter(Q(title__icontains=q) |
        # Q(type__icontains=q))
        q1 = q.title()
        id_type = Type.objects.filter(type__contains=q1)
        categories = Category.objects.raw('SELECT * FROM prokat_category ')
        products = Product.objects.filter(Q(title__contains=q1) | Q(type=id_type))
        # "SELECT * FROM prokat_product WHERE prokat_product.title LIKE '%%%s%%' OR prokat_product.type_id =%s ", (q, q))
        context = {
            'categories': categories,
            'products': products,
            'q': q
        }
        return render(request, 'place_search.html', context)
    return render(request, 'place_search.html')


def check(request):
    form = CheckForm(request.POST or None)
    categories = Category.objects.all()
    if request.method == "POST":
        form = CheckForm(request.POST)
        if form.is_valid():
            dates = form.save(commit=False)
            date1 = dates.date
            date2 = dates.date_end
            #products = Product.objects.all()

            res = Order.objects.values_list('product_id', flat=True).filter(
                Q(date__range=(date1, date2)) | Q(date_end__range=(
                    date1, date2)))
            products = Product.objects.exclude(id__in= res)

            return render(request, 'check.html', {'form': form, 'products': products, 'categories': categories})

        else:
            return render(request, 'check.html',
                          {'form': form, 'text': 'Заполните форму корректно!', 'categories': categories})

    else:
        form = CheckForm()
        return render(request, 'check.html', {'form': form, 'categories': categories})
