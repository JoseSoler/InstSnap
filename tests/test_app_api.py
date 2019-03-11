from unittest import TestCase

from app import app
from flask import json


class TestAppApi(TestCase):
    """
    This class is an Integration Tests
    """

    def test_api_gives_managed_resources(self):
        # given the Database is Running with a fixed dataset

        # when
        response = app.test_client().get('/api')

        # then
        assert response.status_code == 200
        response_payload = json.loads(response.get_data(as_text=True))
        self.assertDictEqual({'instSnap:posts': '/api/posts'}, response_payload, "Unexpected Response From Server")

    def test_api_gives_only_posts_of_user_one(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(user_id=1))

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')

        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        print(response_payload)

        assert len(response_payload) == 288

    def test_api_gives_only_posts_of_user_two(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(user_id=2))

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')

        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        print(response_payload)

        assert len(response_payload) == 749

    def test_api_gives_no_posts_for_non_existent_user(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(user_id=99999999))

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')

        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        print(response_payload)

        assert len(response_payload) == 0

    def test_api_gives_expected_posts_by_text_search(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(text='wow'))

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')


        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        print(response_payload)

        assert len(response_payload) == 1


    def test_api_gives_expected_posts_by_time_range(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(user_id=1,
                                          start_time='2019-03-04-08:00:00',
                                          end_time='2019-03-05-08:00:00'))

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')

        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        print(response_payload)

        assert len(response_payload) == 3

    def test_api_projects_posts_fields(self):
        # given the Database is up and running and
        request_payload = json.dumps(dict(search_fields="user_id text"))
        expected_first_doc = {'text': 'Buena suerte en tu r', 'user_id': 1}

        # when
        response = app.test_client().post('/api/posts/_search',
                                          data=request_payload,
                                          content_type='application/json')

        # then
        assert response.status_code == 200

        response_payload = json.loads(response.get_data(as_text=True))
        self.assertDictEqual(expected_first_doc, response_payload[0], "Projection is not working as expected")

