import datetime
import json
from collections import namedtuple

import requests
from django.conf import settings


class ClientConfigurationError(Exception):
    """Raised when client is misconfigured."""


Video = namedtuple('Video', 'url thumbnail title date')


class YouTubeClient():
    VIDEO_URL_TEMPLATE = 'https://www.youtube.com/watch?v={}'
    SOURCE_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.000Z'

    def __init__(self):
        parts = (
            'snippet',
            'id',
        )
        self.channel_search_base_url = '{}/search'.format(
            settings.YOUTUBE_API_BASE_URL)
        self.channel_search_parameters = {
            'key': settings.YOUTUBE_API_KEY,
            'channelId': settings.YOUTUBE_CHANNEL_ID,
            'part': ','.join(parts),
            'order': 'date',
            'maxResults': settings.YOUTUBE_MAX_RESULTS,
        }

    def list_channel_videos(self):
        response = requests.get(self.channel_search_base_url,
                                params=self.channel_search_parameters)
        content = response.content.decode('utf-8')
        if response.status_code != 200:
            raise ClientConfigurationError(content)
        videos = []

        data = json.loads(content)
        for item in data['items']:
            if item['id']['kind'] != 'youtube#video':
                continue
            snippet = item['snippet']
            published_at = datetime.datetime.strptime(
                snippet['publishedAt'], self.SOURCE_DATE_FORMAT)
            videos.append(Video(
                url=self.VIDEO_URL_TEMPLATE.format(item['id']['videoId']),
                thumbnail=snippet['thumbnails']['medium']['url'],
                title=snippet['title'],
                date=published_at.date(),
            ))

        return videos
