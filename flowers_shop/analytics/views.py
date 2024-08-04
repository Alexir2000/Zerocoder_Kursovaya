# analytics/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Zakaz, Adresa, Otgruzka
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from datetime import datetime

def parse_custom_date(date_str):
    """
    Парсит дату из строки в различных форматах (дд.мм.гггг, дд/мм/гггг, дд.мм, дд/мм)
    и возвращает дату в формате дд.мм.гггг.
    """
    current_year = datetime.now().year
    formats = ["%d.%m.%Y", "%d/%m/%Y", "%d.%m", "%d/%m"]
    for fmt in formats:
        try:
            date = datetime.strptime(date_str, fmt)
            if fmt in ["%d.%m", "%d/%m"]:
                date = date.replace(year=current_year)
            return date.strftime("%d.%m.%Y")
        except ValueError:
            continue
    return None

@login_required
def manager_kabinet(request):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    orders = Zakaz.objects.all().order_by('-DataZakaza')

    # Фильтрация заказов по дате
    filter_date = request.GET.get('filter_date', '')
    if filter_date:
        filter_date = parse_custom_date(filter_date)
        if filter_date:
            date = datetime.strptime(filter_date, "%d.%m.%Y")
            orders = orders.filter(DataZakaza__date=date)

    # Фильтрация заказов по статусу
    filter_status = request.GET.get('filter_status', '')
    if filter_status:
        if filter_status == "sobrano":
            orders = orders.filter(Sobrano=True)
        elif filter_status == "peredano_dostavka":
            orders = orders.filter(Peredano_dostavka=True)
        elif filter_status == "zakaz_dostavlen":
            orders = orders.filter(Zakaz_dostavlen=True)
        elif filter_status == "zakaz_poluchen":
            orders = orders.filter(Zakaz_Poluchen=True)
        elif filter_status == "zakaz_zakryt":
            orders = orders.filter(Zakaz_zakryt=True)

    for order in orders:
        otgruzki = Otgruzka.objects.filter(ID_Zakaz=order)
        order.total_price = sum(item.cena * item.quantity for item in otgruzki)

    context = {
        'orders': orders,
        'filter_date': filter_date,
        'filter_status': filter_status,
    }
    return render(request, 'analytics/manager_kabinet.html', context)


@require_POST
@login_required
def update_order_status(request):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    orders_data = request.POST.dict()
    for key in orders_data.keys():
        if key.startswith('orders[') and key.endswith('][Sobrano]'):
            order_id = key.split('[')[1].split(']')[0]
            order = get_object_or_404(Zakaz, ID=order_id)
            order.Sobrano = 'orders[{}][Sobrano]'.format(order_id) in request.POST
            order.Peredano_dostavka = 'orders[{}][Peredano_dostavka]'.format(order_id) in request.POST
            order.Zakaz_dostavlen = 'orders[{}][Zakaz_dostavlen]'.format(order_id) in request.POST
            order.Zakaz_Poluchen = 'orders[{}][Zakaz_Poluchen]'.format(order_id) in request.POST
            order.Zakaz_zakryt = 'orders[{}][Zakaz_zakryt]'.format(order_id) in request.POST
            order.save()

    return redirect('manager_kabinet')

@login_required
def zakaz_podrobno(request, order_id):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    order = get_object_or_404(Zakaz, ID=order_id)
    otgruzki = Otgruzka.objects.filter(ID_Zakaz=order)
    total_price = sum(item.cena * item.quantity for item in otgruzki)

    context = {
        'order': order,
        'otgruzki': otgruzki,
        'total_price': total_price,
    }
    return render(request, 'analytics/zakaz_podrobno.html', context)




# def analytics_view(request):
#     reports = Otchet.objects.all()
#     return render(request, 'analytics/analytics.html', {'reports': reports})
