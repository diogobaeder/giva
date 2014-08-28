from datetime import date
from unittest.mock import patch

from nose.tools import istest

from base.clients import Video
from base.tests.utils import YouTubeTestCase


class VideosTest(YouTubeTestCase):
    def video_for(self, name):
        now = date.today()
        return Video(
            id=name,
            url='{}-url'.format(name),
            thumbnail='{}-thumb'.format(name),
            title=name.upper(),
            date=now,
        )

    @istest
    @patch('base.clients.YouTubeClient.list_channel_videos')
    def lists_videos_in_page(self, list_channel_videos):
        videos = [
            self.video_for('foo'),
            self.video_for('bar'),
        ]
        list_channel_videos.return_value = videos

        response = self.client.get('/material/videos/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, videos[0].url)
        self.assertContains(response, videos[0].thumbnail)
        self.assertContains(response, videos[0].title)
        self.assertContains(response, videos[1].url)
        self.assertContains(response, videos[1].url)
        self.assertContains(response, videos[1].thumbnail)
        self.assertContains(response, videos[1].title)
