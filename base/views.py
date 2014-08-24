from django.shortcuts import render

from mezzanine.pages.models import Page


def home(request):
    programme = Page.objects.filter(parent__titles='Programa')
    return render(request, 'index.html', {'programme': programme})
