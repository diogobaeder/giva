import datetime
import json
from collections import namedtuple

import requests
from django.conf import settings


class ClientConfigurationError(Exception):
    """Raised when client is misconfigured."""


Video = namedtuple('Video', 'id url thumbnail title date')


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
        data = self.get_video_data()
        videos = []
        self.insert_videos(data, videos)
        return videos

    def insert_videos(self, data, videos):
        for item in data['items']:
            if item['id']['kind'] != 'youtube#video':
                continue
            self.insert_video(item, videos)

    def insert_video(self, item, videos):
        snippet = item['snippet']
        published_at = datetime.datetime.strptime(
            snippet['publishedAt'], self.SOURCE_DATE_FORMAT)
        video_id = item['id']['videoId']
        videos.append(Video(
            id=video_id,
            url=self.VIDEO_URL_TEMPLATE.format(video_id),
            thumbnail=snippet['thumbnails']['medium']['url'],
            title=snippet['title'],
            date=published_at.date(),
        ))

    def get_video_data(self):
        response = requests.get(self.channel_search_base_url,
                                params=self.channel_search_parameters)
        content = response.content.decode('utf-8')
        self.check_status_code(response, content)
        data = json.loads(content)
        return data

    def check_status_code(self, response, content):
        if response.status_code != 200:
            raise ClientConfigurationError(content)
