# analytics/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from main.models import Zakaz, Adresa, Otgruzka
from django.views.decorators.http import require_POST
from django.utils.dateparse import parse_date
from datetime import datetime
from django.views.decorators.cache import cache_control
from django.utils import timezone
import json
from main.models import Zhurnal_status_Zakaza
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def manager_kabinet(request):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    orders = Zakaz.objects.all().order_by('-DataZakaza')

    # Фильтрация заказов по дате
    if 'filter_date' in request.GET:
        filter_date = request.GET['filter_date']
        request.session['filter_date'] = filter_date
    else:
        filter_date = request.session.get('filter_date', '')

    if filter_date:
        filter_date = parse_custom_date(filter_date)
        if filter_date:
            date = datetime.strptime(filter_date, "%d.%m.%Y")
            orders = orders.filter(DataZakaza__date=date)

    # Фильтрация заказов по статусу
    if 'filter_status' in request.GET:
        filter_status = request.GET['filter_status']
        request.session['filter_status'] = filter_status
    else:
        filter_status = request.session.get('filter_status', '')

    if filter_status:
        if filter_status == "sobrano":
            orders = orders.filter(Sobrano=False)
        elif filter_status == "peredano_dostavka":
            orders = orders.filter(Peredano_dostavka=False)
        elif filter_status == "zakaz_dostavlen":
            orders = orders.filter(Zakaz_dostavlen=False)
        elif filter_status == "zakaz_poluchen":
            orders = orders.filter(Zakaz_Poluchen=False)
        elif filter_status == "zakaz_zakryt":
            orders = orders.filter(Zakaz_zakryt=False)

    # Перезагрузка данных заказов
    orders = list(orders)  # Преобразование QuerySet в список для перезагрузки данных

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
def update_order_status(request, order_id):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    # Получение объекта заказа
    order = get_object_or_404(Zakaz, ID=order_id)

    # Получение новых значений из формы
    sobrano_value = request.POST.get(f'orders[{order_id}][Sobrano]', 'off') == 'on'
    peredano_dostavka_value = request.POST.get(f'orders[{order_id}][Peredano_dostavka]', 'off') == 'on'
    zakaz_dostavlen_value = request.POST.get(f'orders[{order_id}][Zakaz_dostavlen]', 'off') == 'on'
    zakaz_poluchen_value = request.POST.get(f'orders[{order_id}][Zakaz_Poluchen]', 'off') == 'on'
    zakaz_zakryt_value = request.POST.get(f'orders[{order_id}][Zakaz_zakryt]', 'off') == 'on'

    current_time = timezone.now()

    def log_change(order, field_name, new_value, description):
        izmenenie = "Выполнено" if new_value else "НЕ выполнено"

        # Создание записи журнала без json_str
        zhurnal_entry = Zhurnal_status_Zakaza.objects.create(
            ID_Zakaza=order,
            Izmenenie=izmenenie,
            pole_izm=description,
            Date=current_time
        )

        # Обновление записи журнала с json_str
        json_data = json.dumps({
            "ID": zhurnal_entry.ID,
            "ID_Zakaza": order.ID,
            "Izmenenie": izmenenie,
            "pole_izm": description,
            "Date": current_time.strftime("%d.%m.%Y %H:%M")
        })

        zhurnal_entry.json_str = json_data
        zhurnal_entry.save()

    # Обновление полей заказа и запись в журнал изменений
    if order.Sobrano != sobrano_value:
        order.Sobrano = sobrano_value
        order.Data_sborki = current_time if sobrano_value else None
        log_change(order, "Sobrano", sobrano_value, "Заказ собран")

    if order.Peredano_dostavka != peredano_dostavka_value:
        order.Peredano_dostavka = peredano_dostavka_value
        order.Data_peredano_v_dostavku = current_time if peredano_dostavka_value else None
        log_change(order, "Peredano_dostavka", peredano_dostavka_value, "Передано в доставку")

    if order.Zakaz_dostavlen != zakaz_dostavlen_value:
        order.Zakaz_dostavlen = zakaz_dostavlen_value
        order.DataDostavki = current_time if zakaz_dostavlen_value else None
        log_change(order, "Zakaz_dostavlen", zakaz_dostavlen_value, "Заказ доставлен")

    if order.Zakaz_Poluchen != zakaz_poluchen_value:
        order.Zakaz_Poluchen = zakaz_poluchen_value
        order.Data_Zakaz_Poluchen = current_time if zakaz_poluchen_value else None
        log_change(order, "Zakaz_Poluchen", zakaz_poluchen_value, "Заказ получен")

    if order.Zakaz_zakryt != zakaz_zakryt_value:
        order.Zakaz_zakryt = zakaz_zakryt_value
        order.Data_Zakaz_zakryt = current_time if zakaz_zakryt_value else None
        log_change(order, "Zakaz_zakryt", zakaz_zakryt_value, "Заказ закрыт")

    # Сохранение заказа
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

@login_required
@csrf_exempt
def clear_zhurnal(request):
    if request.user.StatusID_id != 3:  # Проверка на статус менеджера
        return redirect('index')

    if request.method == "POST":
        # Удаление всех записей из Zhurnal_status_Zakaza
        Zhurnal_status_Zakaza.objects.all().delete()
        messages.success(request, 'Журнал успешно очищен.')
        return redirect('clear_zhurnal')

    return render(request, 'analytics/clear_zhurnal.html')


# def analytics_view(request):
#     reports = Otchet.objects.all()
#     return render(request, 'analytics/analytics.html', {'reports': reports})
