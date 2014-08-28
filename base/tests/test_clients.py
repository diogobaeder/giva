from datetime import date
from unittest.mock import patch

from nose.tools import istest

from base.clients import ClientConfigurationError, YouTubeClient
from base.tests.utils import YouTubeTestCase


class YouTubeClientTest(YouTubeTestCase):
    @istest
    def raises_exception_if_misconfigured_api_key(self):
        client = YouTubeClient()
        client.channel_search_parameters['key'] = ''

        with self.assertRaises(ClientConfigurationError):
            client.list_channel_videos()

    @istest
    @patch('requests.get')
    def lists_available_videos_in_the_channel(self, mock_get):
        response = mock_get.return_value
        response.status_code = 200
        response.content.decode.return_value = self.video_contents()

        client = YouTubeClient()
        videos = client.list_channel_videos()

        self.assertEqual(len(videos), 3)
        video_id = 'J3rGpHlIabY'
        self.assertEqual(videos[0].id, video_id)
        self.assertEqual(videos[0].url, self.url_for(video_id))
        self.assertEqual(videos[0].thumbnail, self.thumb_for(video_id))
        self.assertEqual(videos[0].title, ('Plenária de lançamento da campanha '
                                           'Giva 5006 - Dep. Federal - PSOL'))
        self.assertEqual(videos[0].date, date(2014, 8, 25))

        response.content.decode.assert_called_once_with('utf-8')
