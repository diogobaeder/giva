from django.shortcuts import render

from mezzanine.pages.models import Page

from base.clients import YouTubeClient


def home(request):
    programme = Page.objects.filter(parent__titles='Programa').order_by(
        '_order')
    return render(request, 'index.html', {'programme': programme})


def list_videos(request):
    client = YouTubeClient()
    videos = client.list_channel_videos()
    return render(request, 'videos.html', {'videos': videos})
