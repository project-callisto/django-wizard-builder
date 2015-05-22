from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html', {
        'report_text': request.POST.get('report_text', ''),
    })
