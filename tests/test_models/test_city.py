#!/usr/bin/python3
"""
Unittest for models.city([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import json
import datetime
import models.city
from io import StringIO
from models.city import City
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


class TestAllCityDocstrings(unittest.TestCase):
    def setUp(self):
        self.c0 = City()

    def testModuleDocstring(self):
        self.assertGreater(len(models.city.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.city, "City"))
        self.assertGreater(len(City.__doc__), 1)


class TestCityClass(unittest.TestCase):
    def setUp(self):
        self.c0 = City()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.c0, BaseModel)

    def test_SubClass(self):
        self.assertTrue(issubclass(City, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.c0.id, None)
        self.assertEqual(self.c0.id, str(uuid.UUID(self.c0.id)))

    def test_InstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(City.id)
        with self.assertRaises(AttributeError):
            print(City.created_at)
        with self.assertRaises(AttributeError):
            print(City.updated_at)

    def test_createdAt(self):
        self.assertIsNot(self.c0.created_at, None)
        self.assertEqual(type(self.c0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.c0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.c0.updated_at, None)
        self.assertEqual(type(self.c0.updated_at), datetime.datetime)
        self.assertLess((self.c0.updated_at - self.c0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            c1 = City()
            self.assertEqual(m.call_args.args, (c1, ))
            FileStorage._FileStorage__objects = {}


class TestCityClassAttributes(unittest.TestCase):
    def setUp(self):
        self.c0 = City()

    def testNameAttribute(self):
        self.assertEqual(self.c0.name, City.name)
        self.assertEqual(type(City.name), str)

        self.c0.name = "Detroit"
        self.assertNotEqual(self.c0.name, City.name)
        self.assertEqual(City.name, '')

    def testStateIdAttribute(self):
        self.assertEqual(self.c0.state_id, City.state_id)
        self.assertEqual(type(City.state_id), str)

        self.c0.state_id = str(uuid.uuid4())
        self.assertNotEqual(self.c0.state_id, City.state_id)
        self.assertEqual(City.state_id, '')


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        c1 = City()
        c1.name = "Hong-Kong"
        c1.state_id = str(uuid.uuid4())
        self.assertEqual(str(c1), "[{}] ({}) {}".format(
                         type(c1).__name__, c1.id, c1.__dict__))

    def testPrint(self):
        c1 = City()
        c1.name = "Dubai"
        c1.state_id = str(uuid.uuid4())
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(c1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(c1).__name__,
                             c1.id, c1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        c1 = City()
        prev_time = c1.updated_at
        c1.save()
        self.assertEqual(type(c1.updated_at), datetime.datetime)
        self.assertGreater(c1.updated_at, prev_time)

    def testSaveToStorage(self):
        c1 = City()
        c1.name = "London"
        c1.state_id = str(uuid.uuid4())
        prev_time = c1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            c1.save()
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(c1.updated_at), datetime.datetime)
        self.assertGreater(c1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        c1 = City()
        self.assertEqual(c1.to_dict(),
                         {'__class__': 'City',
                          'updated_at': '{}'.format(c1.updated_at.isoformat()),
                          'created_at': '{}'.format(c1.created_at.isoformat()),
                          'id': c1.id})

    def testToDictionary2(self):
        c1 = City()
        c1.name = "Istanbul"
        s_id = str(uuid.uuid4())
        c1.state_id = s_id
        self.assertEqual(c1.to_dict(),
                         {'__class__': 'City',
                          'updated_at': '{}'.format(c1.updated_at.isoformat()),
                          'created_at': '{}'.format(c1.created_at.isoformat()),
                          'id': c1.id,
                          'name': 'Istanbul',
                          'state_id': s_id})

    def testToDictInvalidArg(self):
        c1 = City()
        with self.assertRaises(TypeError):
            c1.to_dict(5)


class TestCityFromDict(unittest.TestCase):
    def testRecreate(self):
        c1 = City()
        c1_dict = c1.to_dict()

        with patch('models.storage.new') as m:
            c2 = City(**c1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(c1_dict, c2.to_dict())
        self.assertEqual(c1.__dict__, c2.__dict__)
        self.assertIsNot(c1, c2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "City",
                     'name': "Paris",
                     'state_id': str(uuid.uuid4()),
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        c1 = City(**cust_dict)
        self.assertEqual(c1.to_dict(), cust_dict)
        self.assertEqual(type(c1.updated_at), datetime.datetime)
        self.assertGreater(c1.updated_at, c1.created_at)
        self.assertEqual(c1.name, "Paris")


class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        c1 = City("test", "kwargs", unused_id, unused_date)
        self.assertEqual(c1.to_dict(),
                         {'__class__': 'City',
                          'updated_at': '{}'.format(c1.updated_at.isoformat()),
                          'created_at': '{}'.format(c1.created_at.isoformat()),
                          'id': c1.id})
        self.assertNotEqual(c1.id, unused_id)
        self.assertNotEqual(c1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        c1 = City()
        c1.name = "Mexico City"
        c1_dict = c1.to_dict()

        c2 = City("test", str(uuid.uuid4()),
                  datetime.datetime.now(), **c1_dict)
        self.assertEqual(c1_dict, c2.to_dict())
        self.assertEqual(c1.__dict__, c2.__dict__)
        self.assertIsNot(c1, c2)
