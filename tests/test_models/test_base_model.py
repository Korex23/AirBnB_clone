#!/usr/bin/python3
"""
Unittest for models.base_model([..])

This module contains the required tests for the specified module
"""
import unittest
import models.base_model
import uuid
import os
import datetime
from io import StringIO
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open
import json


def setUpModule():
    FileStorage._FileStorage__objects = {}


def tearDownModule():
    FileStorage._FileStorage__objects = {}
    if os.path.exists("file.json"):
        os.remove("file.json")


class TestAllBaseModelDocstrings(unittest.TestCase):
    def setUp(self):
        self.b0 = BaseModel()

    def testModuleDocstring(self):
        self.assertGreater(len(models.base_model.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.base_model, "BaseModel"))
        self.assertGreater(len(BaseModel.__doc__), 1)

    def testStrFnDocstring(self):
        self.assertTrue(hasattr(self.b0, "__str__"))
        self.assertGreater(len(self.b0.__str__.__doc__), 1)

    def testSaveFnDocstring(self):
        self.assertTrue(hasattr(self.b0, "save"))
        self.assertGreater(len(self.b0.save.__doc__), 1)

    def testToDictFnDocstring(self):
        self.assertTrue(hasattr(self.b0, "to_dict"))
        self.assertGreater(len(self.b0.to_dict.__doc__), 1)


class TestBaseModelClass(unittest.TestCase):
    def setUp(self):
        self.b0 = BaseModel()
        self.curr_time = datetime.datetime.now()

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.b0.id, None)
        self.assertEqual(self.b0.id, str(uuid.UUID(self.b0.id)))

    def test_IdInstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(BaseModel.id)

    def test_createdAt(self):
        self.assertIsNot(self.b0.created_at, None)
        self.assertEqual(type(self.b0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.b0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.b0.updated_at, None)
        self.assertEqual(type(self.b0.updated_at), datetime.datetime)
        self.assertLess((self.b0.updated_at - self.b0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            b1 = BaseModel()
            self.assertEqual(m.call_args.args, (b1, ))
            FileStorage._FileStorage__objects = {}


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        b1 = BaseModel()
        self.assertEqual(str(b1), "[{}] ({}) {}".format(
                         type(b1).__name__, b1.id, b1.__dict__))

    def testPrint(self):
        b1 = BaseModel()
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(b1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(b1).__name__,
                             b1.id, b1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        b1 = BaseModel()
        prev_time = b1.updated_at
        b1.save()
        self.assertEqual(type(b1.updated_at), datetime.datetime)
        self.assertGreater(b1.updated_at, prev_time)

    def testSaveToStorage(self):
        b1 = BaseModel()
        prev_time = b1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            b1.save()
            # all_vals = list(map(lambda v: v.to_dict(), all_o.values()))
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(b1.updated_at), datetime.datetime)
        self.assertGreater(b1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        b1 = BaseModel()
        self.assertEqual(b1.to_dict(),
                         {'__class__': 'BaseModel',
                          'updated_at': '{}'.format(b1.updated_at.isoformat()),
                          'created_at': '{}'.format(b1.created_at.isoformat()),
                          'id': b1.id})

    def testToDictionary2(self):
        b1 = BaseModel()
        b1.name = "Tester"
        b1.num = 7
        self.assertEqual(b1.to_dict(),
                         {'__class__': 'BaseModel',
                          'updated_at': '{}'.format(b1.updated_at.isoformat()),
                          'created_at': '{}'.format(b1.created_at.isoformat()),
                          'id': b1.id,
                          'name': 'Tester',
                          'num': 7})

    def testToDictInvalidArg(self):
        b1 = BaseModel()
        with self.assertRaises(TypeError):
            b1.to_dict(5)


class TestBaseModelFromDict(unittest.TestCase):
    def testRecreate(self):
        b1 = BaseModel()
        b1_dict = b1.to_dict()

        with patch('models.storage.new') as m:
            b2 = BaseModel(**b1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(b1_dict, b2.to_dict())
        self.assertEqual(b1.__dict__, b2.__dict__)
        self.assertIsNot(b1, b2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': 'BaseModel',
                     'name': "Te",
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        b1 = BaseModel(**cust_dict)
        self.assertEqual(b1.to_dict(), cust_dict)
        self.assertEqual(type(b1.updated_at), datetime.datetime)
        self.assertGreater(b1.updated_at, b1.created_at)
        self.assertEqual(b1.name, "Te")

    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        b1 = BaseModel("test", "kwargs", unused_id, unused_date)
        self.assertEqual(b1.to_dict(),
                         {'__class__': 'BaseModel',
                          'updated_at': '{}'.format(b1.updated_at.isoformat()),
                          'created_at': '{}'.format(b1.created_at.isoformat()),
                          'id': b1.id})
        self.assertNotEqual(b1.id, unused_id)
        self.assertNotEqual(b1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        b1 = BaseModel()
        b1_dict = b1.to_dict()

        b2 = BaseModel("test", str(uuid.uuid4()),
                       datetime.datetime.now(), **b1_dict)
        self.assertEqual(b1_dict, b2.to_dict())
        self.assertEqual(b1.__dict__, b2.__dict__)
        self.assertIsNot(b1, b2)
