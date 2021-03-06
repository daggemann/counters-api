import json

from api import db
from api.models import Counter
from api.tests.base import BaseTestCase


class TestCounterEndpoint(BaseTestCase):

    def test_get_all_counters(self):
        """
            Ensure that we can get all counters.
        """
        counter1 = Counter("test1")
        counter1.count = 1
        counter2 = Counter("test2")
        counter2.count = 2
        db.session.add(counter1)
        db.session.add(counter2)
        db.session.commit()

        with self.client:
            response = self.client.get('/counters', content_type='application/json')
            counters = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(counters), 2)
            self.assertDictEqual(counters[0], {'id': 1, 'title': "test1", 'count': 1})
            self.assertDictEqual(counters[1], {'id': 2, 'title': "test2", 'count': 2})

    def test_increment_counter(self):
        """
            Ensure that we can increment a counter, and that we get back all counters.
        """
        counter1 = Counter("test1")
        counter2 = Counter("test2")
        counter2.count = 2
        db.session.add(counter1)
        db.session.add(counter2)
        db.session.commit()

        with self.client:
            response = self.client.post(f'/counters/{counter1.id}/increment', content_type='application/json')
            counters = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(counters), 2)
            self.assertEqual(counters[0]['count'], 1)

    def test_increment_counter_invalid_id(self):
        """
            Ensure that endpoint returns 404 with message when id is not found.
        """
        with self.client:
            response = self.client.post(f'/counters/1/increment', content_type='application/json')
            message = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertDictEqual(message, {'status': 'error', 'reason': 'Resource not found.'})

    def test_decrement_counter(self):
        """
            Ensure that we can decrement a counter, and that we get back all counters.
        :return:
        """
        counter1 = Counter("test1")
        counter1.count = 0
        counter2 = Counter("test2")
        counter2.count = 2
        db.session.add(counter1)
        db.session.add(counter2)
        db.session.commit()

        with self.client:
            response = self.client.post(f'/counters/{counter1.id}/decrement', content_type='application/json')
            counters = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(counters), 2)
            self.assertEqual(counters[0]['count'], -1)

    def test_decrement_counter_invalid_id(self):
        """
            Ensure that endpoint returns 404 with message when id is not found.
        """
        with self.client:
            response = self.client.post(f'/counters/1/decrement', content_type='application/json')
            message = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertDictEqual(message, {'status': 'error', 'reason': 'Resource not found.'})

    def test_delete_counter(self):
        """
            Ensure that we can delete a counter, and that we get back all other counters.
        """
        counter1 = Counter("test1")
        counter1.count = 0
        counter2 = Counter("test2")
        counter2.count = 2
        db.session.add(counter1)
        db.session.add(counter2)
        db.session.commit()

        with self.client:
            response = self.client.delete(f'/counters/{counter1.id}', content_type='application/json')
            counters = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(counters), 1)
            self.assertEqual(counters[0]['title'], "test2")

    def test_delete_counter_invalid_id(self):
        """
            Ensure that endpoint returns 404 with message when id is not found.
        """
        with self.client:
            response = self.client.delete(f'/counters/1')
            message = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 404)
            self.assertDictEqual(message, {'status': 'error', 'reason': 'Resource not found.'})

    def test_add_counter(self):
        """
            Ensure that we can add a new counter which is given an initial count of 0,
            and that we get back all other counters.
        """
        counter1 = Counter("test1")
        counter1.count = 0
        db.session.add(counter1)
        db.session.commit()

        with self.client:
            response = self.client.post(f'/counters',
                                        data=json.dumps({
                                            'title': 'test2'
                                        }),
                                        content_type='application/json')
            counters = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertEqual(len(counters), 2)
            self.assertEqual(counters[1]['title'], "test2")
            self.assertEqual(counters[1]['count'], 0)

    def test_add_counter_missing_title_in_payload(self):
        """
            Ensure that enpoint returns with 400 and message when title is missing from payload.
        """
        with self.client:
            response = self.client.post(f'/counters',
                                        data=json.dumps({}),
                                        content_type='application/json')
            message = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(message, {'status': 'error', 'reason': 'Invalid payload.'})

    def test_add_counter_empty_title_in_payload(self):
        """
            Ensure that enpoint returns with 400 and message when title is empty in payload.
        """
        with self.client:
            response = self.client.post(f'/counters',
                                        data=json.dumps({'title': ''}),
                                        content_type='application/json')
            message = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertDictEqual(message, {'status': 'error', 'reason': 'Invalid payload.'})
