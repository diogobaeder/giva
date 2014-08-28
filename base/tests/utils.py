import json
from os.path import dirname, join
from django.test import TestCase


class YouTubeTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.channel_videos = join(
            dirname(__file__), 'fixtures', 'channel-videos.json')

    def video_contents(self):
        with open(self.channel_videos, encoding='utf-8') as f:
            return f.read()

    def video_json(self):
        return json.loads(self.video_contents())

    def url_for(self, video_id):
        return 'https://www.youtube.com/watch?v={}'.format(video_id)

    def thumb_for(self, video_id):
        return 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(video_id)
