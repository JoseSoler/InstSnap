from datetime import datetime
from unittest import TestCase
from model.post import Post


class TestPost(TestCase):
    """
    A Unit Test for testing the behaviour of Post class
    """

    def test_should_convert_to_dictionary(self):

        # given
        post = Post('myId', 'myUserId', datetime.fromisoformat('2019-03-10'), 'My post text', 'http://someimage', 24)

        expected_dict = {'_id': 'myId',
                         'created_at': datetime.fromisoformat('2019-03-10'),
                         'expires_at': datetime.fromisoformat('2019-03-11'),
                         'image_url': 'http://someimage',
                         'text': 'My post text',
                         'ttl_in_hours': 24,
                         'user_id': 'myUserId'}

        # when
        post_dict = post.to_dictionary()

        # then
        self.assertDictEqual(expected_dict, post_dict, "Dictionaries are not equal, check conversion!")
