from api import db
from api.models import Counter
from api.tests.base import BaseTestCase


class TestCounterModel(BaseTestCase):

    def test_new_counter(self):
        """
            Ensure that a new counter is given a title, and an initial count equal to zero.
        """
        counter = Counter("test")
        self.assertEqual(counter.title, "test")
        self.assertEqual(counter.count, 0)

    def test_add_new_counter_to_database(self):
        """
            Ensure that we can persist a new counter to the database.
        """
        counter = Counter("test")
        counter.add_and_commit()

        counter = db.session.query(Counter).filter(Counter.id == counter.id).first()
        self.assertEqual(counter.title, "test")
        self.assertEqual(counter.count, 0)

    def test_update_counter_to_database(self):
        """
            Ensure that we can update any changes to the counter to the database.
        """

        counter = Counter("test")
        counter.add_and_commit()

        counter.title = "test2"
        counter.count += 1
        counter.commit()

        counter = db.session.query(Counter).filter(Counter.id == counter.id).first()

        self.assertEqual(counter.title, "test2")
        self.assertEqual(counter.count, 1)

    def test_delete_counter_from_database(self):
        """
            Ensure that we can delete a counter from the database.
        """
        counter = Counter("test")
        counter.add_and_commit()
        counter.delete_and_commit()

        counter = db.session.query(Counter).filter(Counter.id == counter.id).first()
        self.assertIsNone(counter)

    def test_get_all_counters_from_database(self):
        """
            Ensure that we can get all counters from the database.
        """
        counter1 = Counter("test1")
        counter2 = Counter("test2")

        db.session.add(counter1)
        db.session.add(counter2)
        db.session.commit()

        counters = Counter.get_all()

        self.assertEqual(len(counters), 2)
        self.assertEqual(counters[0].title, "test1")
        self.assertEqual(counters[1].title, "test2")

    def test_convert_counter_to_dict(self):
        """
            Ensure that we can convert the counter to a dictionary representation.
        """
        counter = Counter("test")
        counter.add_and_commit()

        counter_dict = counter.to_dict()
        self.assertDictEqual(counter_dict, {'id': 1, 'title': "test", 'count': 0})

    def test_get_counter_by_id(self):
        """
            Ensure that we can get a counter by it's id.
        """
        counter = Counter("test")
        counter.add_and_commit()

        counter = Counter.get_by_id(counter.id)
        self.assertEqual(counter.id, 1)
