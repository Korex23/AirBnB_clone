#!/usr/bin/python3
"""
Unittest for models.review([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import json
import datetime
import models.review
from io import StringIO
from models.review import Review
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open


def setUpModule():
    FileStorage._FileStorage__objects = {}


def tearDownModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


class TestAllReviewDocstrings(unittest.TestCase):
    def setUp(self):
        self.r0 = Review()

    def testModuleDocstring(self):
        self.assertGreater(len(models.review.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.review, "Review"))
        self.assertGreater(len(Review.__doc__), 1)


class TestReviewClass(unittest.TestCase):
    def setUp(self):
        self.r0 = Review()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.r0, BaseModel)

    def test_SubClass(self):
        self.assertTrue(issubclass(Review, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.r0.id, None)
        self.assertEqual(self.r0.id, str(uuid.UUID(self.r0.id)))

    def test_InstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(Review.id)
        with self.assertRaises(AttributeError):
            print(Review.created_at)
        with self.assertRaises(AttributeError):
            print(Review.updated_at)

    def test_createdAt(self):
        self.assertIsNot(self.r0.created_at, None)
        self.assertEqual(type(self.r0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.r0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.r0.updated_at, None)
        self.assertEqual(type(self.r0.updated_at), datetime.datetime)
        self.assertLess((self.r0.updated_at - self.r0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            r1 = Review()
            self.assertEqual(m.call_args.args, (r1, ))
            FileStorage._FileStorage__objects = {}


class TestReviewClassAttributes(unittest.TestCase):
    def setUp(self):
        self.r0 = Review()

    def testPlaceIdAttribute(self):
        self.assertEqual(self.r0.place_id, Review.place_id)
        self.assertEqual(type(Review.place_id), str)

        self.r0.place_id = str(uuid.uuid4())
        self.assertNotEqual(self.r0.place_id, Review.place_id)
        self.assertEqual(Review.place_id, '')

    def testUserIdAttribute(self):
        self.assertEqual(self.r0.user_id, Review.user_id)
        self.assertEqual(type(Review.user_id), str)

        self.r0.user_id = str(uuid.uuid4())
        self.assertNotEqual(self.r0.user_id, Review.user_id)
        self.assertEqual(Review.user_id, '')

    def testTextAttribute(self):
        self.assertEqual(self.r0.text, Review.text)
        self.assertEqual(type(Review.text), str)

        self.r0.text = "Perfect"
        self.assertNotEqual(self.r0.text, Review.text)
        self.assertEqual(Review.text, '')


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        r1 = Review()
        r1.place_id = str(uuid.uuid4())
        r1.user_id = str(uuid.uuid4())
        r1.text = "Totally Recommend"
        self.assertEqual(str(r1), "[{}] ({}) {}".format(
                         type(r1).__name__, r1.id, r1.__dict__))

    def testPrint(self):
        r1 = Review()
        r1.place_id = str(uuid.uuid4())
        r1.user_id = str(uuid.uuid4())
        r1.text = "Waste of time"
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(r1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(r1).__name__,
                             r1.id, r1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        r1 = Review()
        prev_time = r1.updated_at
        r1.save()
        self.assertEqual(type(r1.updated_at), datetime.datetime)
        self.assertGreater(r1.updated_at, prev_time)

    def testSaveToStorage(self):
        r1 = Review()
        r1.place_id = str(uuid.uuid4())
        r1.user_id = str(uuid.uuid4())
        r1.text = "Look forward to returning"
        prev_time = r1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            r1.save()
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(r1.updated_at), datetime.datetime)
        self.assertGreater(r1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        r1 = Review()
        self.assertEqual(r1.to_dict(),
                         {'__class__': 'Review',
                          'updated_at': '{}'.format(r1.updated_at.isoformat()),
                          'created_at': '{}'.format(r1.created_at.isoformat()),
                          'id': r1.id})

    def testToDictionary2(self):
        r1 = Review()
        r1.place_id = str(uuid.uuid4())
        r1.user_id = str(uuid.uuid4())
        r1.text = "5 Star any day(night)."
        self.assertEqual(r1.to_dict(),
                         {'__class__': 'Review',
                          'updated_at': '{}'.format(r1.updated_at.isoformat()),
                          'created_at': '{}'.format(r1.created_at.isoformat()),
                          'id': r1.id,
                          'place_id': r1.place_id,
                          'user_id': r1.user_id,
                          'text': "5 Star any day(night)."})

    def testToDictInvalidArg(self):
        r1 = Review()
        with self.assertRaises(TypeError):
            r1.to_dict(5)


class TestReviewFromDict(unittest.TestCase):
    def testRecreate(self):
        r1 = Review()
        r1_dict = r1.to_dict()

        with patch('models.storage.new') as m:
            r2 = Review(**r1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(r1_dict, r2.to_dict())
        self.assertEqual(r1.__dict__, r2.__dict__)
        self.assertIsNot(r1, r2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "Review",
                     'text': "Absolute waste of time",
                     'place_id': str(uuid.uuid4()),
                     'user_id': str(uuid.uuid4()),
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        r1 = Review(**cust_dict)
        self.assertEqual(r1.to_dict(), cust_dict)
        self.assertEqual(type(r1.updated_at), datetime.datetime)
        self.assertGreater(r1.updated_at, r1.created_at)
        self.assertEqual(r1.text, "Absolute waste of time")


class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        r1 = Review("test", "kwargs", unused_id, unused_date)
        self.assertEqual(r1.to_dict(),
                         {'__class__': 'Review',
                          'updated_at': '{}'.format(r1.updated_at.isoformat()),
                          'created_at': '{}'.format(r1.created_at.isoformat()),
                          'id': r1.id})
        self.assertNotEqual(r1.id, unused_id)
        self.assertNotEqual(r1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        r1 = Review()
        r1.text = "Not bad for $100 stay."
        r1_dict = r1.to_dict()

        r2 = Review("test", str(uuid.uuid4()),
                    datetime.datetime.now(), **r1_dict)
        self.assertEqual(r1_dict, r2.to_dict())
        self.assertEqual(r1.__dict__, r2.__dict__)
        self.assertIsNot(r1, r2)
