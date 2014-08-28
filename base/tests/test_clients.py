from datetime import date
from os.path import dirname, join
from unittest import TestCase
from unittest.mock import patch

from requests import HTTPError
from nose.tools import istest

from base.clients import ClientConfigurationError, YouTubeClient


class YouTubeClientTest(TestCase):
    def setUp(self):
        self.channel_videos = join(
            dirname(__file__), 'fixtures', 'channel-videos.json')

    def url_for(self, video_id):
        return 'https://www.youtube.com/watch?v={}'.format(video_id)

    def thumb_for(self, video_id):
        return 'https://i.ytimg.com/vi/{}/mqdefault.jpg'.format(video_id)

    @istest
    def raises_exception_if_misconfigured_api_key(self):
        client = YouTubeClient()
        client.channel_search_parameters['key'] = ''

        with self.assertRaises(ClientConfigurationError):
            client.list_channel_videos()

    @istest
    @patch('requests.get')
    def lists_available_videos_in_the_channel(self, mock_get):
        with open(self.channel_videos, encoding='utf-8') as f:
            response = mock_get.return_value
            response.status_code = 200
            response.content.decode.return_value = f.read()

        client = YouTubeClient()
        videos = client.list_channel_videos()

        self.assertEqual(len(videos), 3)
        self.assertEqual(videos[0].url, self.url_for('J3rGpHlIabY'))
        self.assertEqual(videos[0].thumbnail, self.thumb_for('J3rGpHlIabY'))
        self.assertEqual(videos[0].title, ('Plenária de lançamento da campanha '
                                           'Giva 5006 - Dep. Federal - PSOL'))
        self.assertEqual(videos[0].date, date(2014, 8, 25))

        response.content.decode.assert_called_once_with('utf-8')
