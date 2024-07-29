from django.shortcuts import render
from main.models import Otchet

def analytics_view(request):
    reports = Otchet.objects.all()
    return render(request, 'analytics/analytics.html', {'reports': reports})
