#!/usr/bin/python3
"""
Unittest for models.state([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import datetime
import json
import models.state
from io import StringIO
from models.state import State
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


class TestAllStateDocstrings(unittest.TestCase):
    def setUp(self):
        self.s0 = State()

    def testModuleDocstring(self):
        self.assertGreater(len(models.state.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.state, "State"))
        self.assertGreater(len(State.__doc__), 1)


class TestStateClass(unittest.TestCase):
    def setUp(self):
        self.s0 = State()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.s0, State)

    def test_SubClass(self):
        self.assertTrue(issubclass(State, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.s0.id, None)
        self.assertEqual(self.s0.id, str(uuid.UUID(self.s0.id)))

    def test_InstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(State.id)
        with self.assertRaises(AttributeError):
            print(State.created_at)
        with self.assertRaises(AttributeError):
            print(State.updated_at)

    def test_createdAt(self):
        self.assertIsNot(self.s0.created_at, None)
        self.assertEqual(type(self.s0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.s0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.s0.updated_at, None)
        self.assertEqual(type(self.s0.updated_at), datetime.datetime)
        self.assertLess((self.s0.updated_at - self.s0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            s1 = State()
            self.assertEqual(m.call_args.args, (s1, ))
            FileStorage._FileStorage__objects = {}


class TestStateClassAttributes(unittest.TestCase):
    def testNameAttribute(self):
        s1 = State()
        self.assertEqual(s1.name, State.name)
        self.assertEqual(type(State.name), str)

        s1.name = "LA"
        self.assertNotEqual(s1.name, State.name)
        self.assertEqual(State.name, '')


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        s1 = State()
        s1.name = "Kigali"
        self.assertEqual(str(s1), "[{}] ({}) {}".format(
                         type(s1).__name__, s1.id, s1.__dict__))

    def testPrint(self):
        s1 = State()
        s1.name = "Kampala"
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(s1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(s1).__name__,
                             s1.id, s1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        s1 = State()
        prev_time = s1.updated_at
        s1.save()
        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, prev_time)

    def testSaveToStorage(self):
        s1 = State()
        s1.name = "Los-Angeles"
        prev_time = s1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            s1.save()
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        s1 = State()
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id})

    def testToDictionary2(self):
        s1 = State()
        s1.name = "Texas"
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id,
                          'name': 'Texas'})

    def testToDictInvalidArg(self):
        s1 = State()
        with self.assertRaises(TypeError):
            s1.to_dict(5)


class TestBaseModelFromDict(unittest.TestCase):
    def testRecreate(self):
        s1 = State()
        s1_dict = s1.to_dict()

        with patch('models.storage.new') as m:
            s2 = State(**s1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(s1_dict, s2.to_dict())
        self.assertEqual(s1.__dict__, s2.__dict__)
        self.assertIsNot(s1, s2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "State",
                     'name': "Lagos",
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        s1 = State(**cust_dict)
        self.assertEqual(s1.to_dict(), cust_dict)
        self.assertEqual(type(s1.updated_at), datetime.datetime)
        self.assertGreater(s1.updated_at, s1.created_at)
        self.assertEqual(s1.name, "Lagos")


class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        s1 = State("test", "kwargs", unused_id, unused_date)
        self.assertEqual(s1.to_dict(),
                         {'__class__': 'State',
                          'updated_at': '{}'.format(s1.updated_at.isoformat()),
                          'created_at': '{}'.format(s1.created_at.isoformat()),
                          'id': s1.id})
        self.assertNotEqual(s1.id, unused_id)
        self.assertNotEqual(s1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        s1 = BaseModel()
        s1_dict = s1.to_dict()

        s2 = BaseModel("test", str(uuid.uuid4()),
                       datetime.datetime.now(), **s1_dict)
        self.assertEqual(s1_dict, s2.to_dict())
        self.assertEqual(s1.__dict__, s2.__dict__)
        self.assertIsNot(s1, s2)
