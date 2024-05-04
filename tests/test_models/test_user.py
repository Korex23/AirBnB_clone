#!/usr/bin/python3
"""
Unittest for models.user([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import json
import datetime
import models.user
from io import StringIO
from models.user import User
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


class TestAllUserDocstrings(unittest.TestCase):
    def setUp(self):
        self.u0 = User()

    def testModuleDocstring(self):
        self.assertGreater(len(models.user.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.user, "User"))
        self.assertGreater(len(User.__doc__), 1)


class TestUserClass(unittest.TestCase):
    def setUp(self):
        self.u0 = User()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.u0, BaseModel)

    def test_SubClass(self):
        self.assertTrue(issubclass(User, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.u0.id, None)
        self.assertEqual(self.u0.id, str(uuid.UUID(self.u0.id)))

    def test_InstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(User.id)
        with self.assertRaises(AttributeError):
            print(User.created_at)
        with self.assertRaises(AttributeError):
            print(User.updated_at)

    def test_createdAt(self):
        self.assertIsNot(self.u0.created_at, None)
        self.assertEqual(type(self.u0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.u0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.u0.updated_at, None)
        self.assertEqual(type(self.u0.updated_at), datetime.datetime)
        self.assertLess((self.u0.updated_at - self.u0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            u1 = User()
            self.assertEqual(m.call_args.args, (u1, ))
            FileStorage._FileStorage__objects = {}


class TestUserClassAttributes(unittest.TestCase):
    def setUp(self):
        self.u0 = User()

    def testEmailAttribute(self):
        self.assertEqual(self.u0.email, User.email)
        self.assertEqual(type(User.email), str)

        self.u0.email = "airbnb2@mail.com"
        self.assertNotEqual(self.u0.email, User.email)
        self.assertEqual(User.email, '')

    def testPasswordAttribute(self):
        self.assertEqual(self.u0.password, User.password)
        self.assertEqual(type(User.password), str)

        self.u0.password = "root"
        self.assertNotEqual(self.u0.password, User.password)
        self.assertEqual(User.password, '')

    def testFirstNameAttribute(self):
        self.assertEqual(self.u0.first_name, User.first_name)
        self.assertEqual(type(User.first_name), str)

        self.u0.first_name = "Betty"
        self.assertNotEqual(self.u0.first_name, User.first_name)
        self.assertEqual(User.password, '')

    def testLastNameAttribute(self):
        self.assertEqual(self.u0.last_name, User.last_name)
        self.assertEqual(type(User.last_name), str)

        self.u0.last_name = "Butter"
        self.assertNotEqual(self.u0.last_name, User.last_name)
        self.assertEqual(User.last_name, '')


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        u1 = User()
        u1.first_name = "Betty"
        u1.last_name = "Butter"
        u1.email = "airbnb@mail.com"
        u1.password = "root"
        self.assertEqual(str(u1), "[{}] ({}) {}".format(
                         type(u1).__name__, u1.id, u1.__dict__))

    def testPrint(self):
        u1 = User()
        u1.last_name = "Bar"
        u1.email = "airbnb@mail.com"
        u1.password = "root"
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(u1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(u1).__name__,
                             u1.id, u1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        u1 = User()
        prev_time = u1.updated_at
        u1.save()
        self.assertEqual(type(u1.updated_at), datetime.datetime)
        self.assertGreater(u1.updated_at, prev_time)

    def testSaveToStorage(self):
        u1 = User()
        u1.email = "airbnb@mail.com"
        u1.password = "root"
        prev_time = u1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            u1.save()
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(u1.updated_at), datetime.datetime)
        self.assertGreater(u1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        u1 = User()
        self.assertEqual(u1.to_dict(),
                         {'__class__': 'User',
                          'updated_at': '{}'.format(u1.updated_at.isoformat()),
                          'created_at': '{}'.format(u1.created_at.isoformat()),
                          'id': u1.id})

    def testToDictionary2(self):
        u1 = User()
        u1.first_name = "Betty"
        u1.last_name = "Butter"
        u1.email = "airbnb@gmail.com"
        u1.password = "root"
        self.assertEqual(u1.to_dict(),
                         {'__class__': 'User',
                          'updated_at': '{}'.format(u1.updated_at.isoformat()),
                          'created_at': '{}'.format(u1.created_at.isoformat()),
                          'id': u1.id,
                          'first_name': 'Betty',
                          'last_name': 'Butter',
                          'email': 'airbnb@gmail.com',
                          'password': 'root'})

    def testToDictInvalidArg(self):
        u1 = User()
        with self.assertRaises(TypeError):
            u1.to_dict(5)


class TestUserFromDict(unittest.TestCase):
    def testRecreate(self):
        u1 = User()
        u1_dict = u1.to_dict()

        with patch('models.storage.new') as m:
            u2 = User(**u1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(u1_dict, u2.to_dict())
        self.assertEqual(u1.__dict__, u2.__dict__)
        self.assertIsNot(u1, u2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "User",
                     'first_name': "Y",
                     'last_name': "Inim",
                     'email': "airbnb@mail.com",
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        u1 = User(**cust_dict)
        self.assertEqual(u1.to_dict(), cust_dict)
        self.assertEqual(type(u1.updated_at), datetime.datetime)
        self.assertGreater(u1.updated_at, u1.created_at)
        self.assertEqual(u1.first_name, "Y")


class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        u1 = User("test", "kwargs", unused_id, unused_date)
        self.assertEqual(u1.to_dict(),
                         {'__class__': 'User',
                          'updated_at': '{}'.format(u1.updated_at.isoformat()),
                          'created_at': '{}'.format(u1.created_at.isoformat()),
                          'id': u1.id})
        self.assertNotEqual(u1.id, unused_id)
        self.assertNotEqual(u1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        u1 = User()
        u1_dict = u1.to_dict()

        u2 = User("test", str(uuid.uuid4()),
                  datetime.datetime.now(), **u1_dict)
        self.assertEqual(u1_dict, u2.to_dict())
        self.assertEqual(u1.__dict__, u2.__dict__)
        self.assertIsNot(u1, u2)
