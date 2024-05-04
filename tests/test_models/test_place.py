#!/usr/bin/python3
"""
Unittest for models.place([..])

This module contains the required tests for the specified module
"""
import unittest
import uuid
import os
import json
import datetime
import models.place
from io import StringIO
from models.place import Place
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


class TestAllPlaceDocstrings(unittest.TestCase):
    def setUp(self):
        self.p0 = Place()

    def testModuleDocstring(self):
        self.assertGreater(len(models.place.__doc__), 1)

    def testClassDocstring(self):
        self.assertTrue(hasattr(models.place, "Place"))
        self.assertGreater(len(Place.__doc__), 1)


class TestPlaceClass(unittest.TestCase):
    def setUp(self):
        self.p0 = Place()
        self.curr_time = datetime.datetime.now()

    def test_Instance(self):
        self.assertIsInstance(self.p0, BaseModel)

    def test_SubClass(self):
        self.assertTrue(issubclass(Place, BaseModel))

    def test_Id(self):
        # Test that id is valid uuid
        self.assertIsNot(self.p0.id, None)
        self.assertEqual(self.p0.id, str(uuid.UUID(self.p0.id)))

    def test_InstanceVariable(self):
        with self.assertRaises(AttributeError):
            print(Place.id)
        with self.assertRaises(AttributeError):
            print(Place.created_at)
        with self.assertRaises(AttributeError):
            print(Place.updated_at)

    def test_createdAt(self):
        self.assertIsNot(self.p0.created_at, None)
        self.assertEqual(type(self.p0.created_at), datetime.datetime)
        self.assertLess((self.curr_time - self.p0.created_at).
                        total_seconds(), 0.001)

    def test_updatedAt(self):
        self.assertIsNot(self.p0.updated_at, None)
        self.assertEqual(type(self.p0.updated_at), datetime.datetime)
        self.assertLess((self.p0.updated_at - self.p0.created_at).
                        total_seconds(), 0.001)

    def testInstantiationWithNew(self):
        with patch('models.storage.new') as m:
            p1 = Place()
            self.assertEqual(m.call_args.args, (p1, ))
            FileStorage._FileStorage__objects = {}


class TestPlaceClassAttributes(unittest.TestCase):
    def setUp(self):
        self.p0 = Place()

    def testCityIdAttribute(self):
        self.assertEqual(self.p0.city_id, Place.city_id)
        self.assertEqual(type(Place.city_id), str)

        self.p0.city_id = str(uuid.uuid4())
        self.assertNotEqual(self.p0.city_id, Place.city_id)
        self.assertEqual(Place.city_id, '')

    def testUserIdAttribute(self):
        self.assertEqual(self.p0.user_id, Place.user_id)
        self.assertEqual(type(Place.user_id), str)

        self.p0.user_id = str(uuid.uuid4())
        self.assertNotEqual(self.p0.user_id, Place.user_id)
        self.assertEqual(Place.user_id, '')

    def testNameAttribute(self):
        self.assertEqual(self.p0.name, Place.name)
        self.assertEqual(type(Place.name), str)

        self.p0.name = "La Casa"
        self.assertNotEqual(self.p0.name, Place.name)
        self.assertEqual(Place.name, '')

    def testDescriptionAttribute(self):
        self.assertEqual(self.p0.description, Place.description)
        self.assertEqual(type(Place.description), str)

        self.p0.description = "Mountain and Ocean View"
        self.assertNotEqual(self.p0.description, Place.description)
        self.assertEqual(Place.description, '')

    def testNumberRoomsAttribute(self):
        self.assertEqual(self.p0.number_rooms, Place.number_rooms)
        self.assertEqual(type(Place.number_rooms), int)

        self.p0.number_rooms = 7
        self.assertNotEqual(self.p0.number_rooms, Place.number_rooms)
        self.assertEqual(Place.number_rooms, 0)

    def testNumberBathroomsAttribute(self):
        self.assertEqual(self.p0.number_bathrooms, Place.number_bathrooms)
        self.assertEqual(type(Place.number_bathrooms), int)

        self.p0.number_bathrooms = 4
        self.assertNotEqual(self.p0.number_bathrooms, Place.number_bathrooms)
        self.assertEqual(Place.number_bathrooms, 0)

    def testMaxGuestAttribute(self):
        self.assertEqual(self.p0.max_guest, Place.max_guest)
        self.assertEqual(type(Place.max_guest), int)

        self.p0.max_guest = 12
        self.assertNotEqual(self.p0.max_guest, Place.max_guest)
        self.assertEqual(Place.max_guest, 0)

    def testPriceByNightAttribute(self):
        self.assertEqual(self.p0.price_by_night, Place.price_by_night)
        self.assertEqual(type(Place.price_by_night), int)

        self.p0.price_by_night = 112
        self.assertNotEqual(self.p0.price_by_night, Place.price_by_night)
        self.assertEqual(Place.price_by_night, 0)

    def testLatitudeAttribute(self):
        self.assertEqual(self.p0.latitude, Place.latitude)
        self.assertEqual(type(Place.latitude), float)

        self.p0.latitude = 5.357
        self.assertNotEqual(self.p0.latitude, Place.latitude)
        self.assertEqual(Place.latitude, 0.0)

    def testLongitudeAttribute(self):
        self.assertEqual(self.p0.longitude, Place.longitude)
        self.assertEqual(type(Place.longitude), float)

        self.p0.longitude = 10.257
        self.assertNotEqual(self.p0.longitude, Place.longitude)
        self.assertEqual(Place.longitude, 0.0)

    def testAmenityIdsAttribute(self):
        self.assertEqual(self.p0.amenity_ids, Place.amenity_ids)
        self.assertEqual(type(Place.amenity_ids), list)

        self.p0.amenity_ids = [str(uuid.uuid4())]
        self.assertNotEqual(self.p0.amenity_ids, Place.amenity_ids)
        self.assertEqual(Place.amenity_ids, [])


class TestStrMethod(unittest.TestCase):
    def testStr(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.user_id = str(uuid.uuid4())
        p1.name = "Casa Rodolfo"
        p1.description = "Cozy penthouse with beautiful land view"
        p1.number_rooms = 2
        p1.number_bathrooms = 2
        p1.max_guest = 4
        p1.price_by_night = 138
        p1.latitude = 5.734
        p1.longitude = 10.2456
        p1.amenity_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        self.assertEqual(str(p1), "[{}] ({}) {}".format(
                         type(p1).__name__, p1.id, p1.__dict__))

    def testPrint(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.user_id = str(uuid.uuid4())
        p1.name = "Drago Apartment"
        p1.description = "Exclusive Apartments"
        p1.number_rooms = 1
        p1.number_bathrooms = 1
        p1.max_guest = 2
        p1.price_by_night = 102
        p1.latitude = 31.4567
        p1.longitude = 15.3426
        p1.amenity_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        with patch("sys.stdout", new=StringIO()) as mock_print:
            print(p1)
            self.assertEqual(mock_print.getvalue(), "[{}] ({}) {}\n".
                             format(type(p1).__name__,
                             p1.id, p1.__dict__))


class TestSaveMethod(unittest.TestCase):
    def testDateTimeUpdate(self):
        p1 = Place()
        prev_time = p1.updated_at
        p1.save()
        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, prev_time)

    def testSaveToStorage(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.user_id = str(uuid.uuid4())
        p1.name = "The Potter's"
        p1.number_rooms = 4
        p1.price_by_night = 150
        p1.latitude = 21.3453
        p1.longitude = 16.1226
        p1.amenity_ids = [str(uuid.uuid4()), str(uuid.uuid4())]
        prev_time = p1.updated_at
        fname = "file.json"
        all_o = storage.all()
        al_k = ['{}.{}'.format(type(o).__name__, o.id) for o in all_o.values()]
        with patch("models.engine.file_storage.open", mock_open()) as mock_f:
            p1.save()
            f_dict = {k: v.to_dict() for k, v in zip(al_k, all_o.values())}
            fcontent = json.dumps(f_dict)
            mock_f.assert_called_once_with(fname, 'w', encoding='utf-8')
        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, prev_time)


class TestToDictMethod(unittest.TestCase):
    def testToDictionary(self):
        p1 = Place()
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id})

    def testToDictionary2(self):
        p1 = Place()
        p1.city_id = str(uuid.uuid4())
        p1.name = "The Squire's Field"
        p1.number_rooms = 12
        p1.price_by_night = 133
        p1.latitude = 15.6781
        p1.longitude = 2.345
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id,
                          'city_id': p1.city_id,
                          'name': "The Squire's Field",
                          'number_rooms': 12,
                          'price_by_night': 133,
                          'longitude': 2.345,
                          'latitude': 15.6781})

    def testToDictInvalidArg(self):
        p1 = Place()
        with self.assertRaises(TypeError):
            p1.to_dict(5)


class TestPlaceFromDict(unittest.TestCase):
    def testRecreate(self):
        p1 = Place()
        p1_dict = p1.to_dict()

        with patch('models.storage.new') as m:
            p2 = Place(**p1_dict)
            self.assertIs(m.call_args, None)

        self.assertEqual(p1_dict, p2.to_dict())
        self.assertEqual(p1.__dict__, p2.__dict__)
        self.assertIsNot(p1, p2)

    def testCreateFromCustomDict(self):
        c_ti = datetime.datetime.now()
        o_d = datetime.timedelta(days=1)
        cust_dict = {'__class__': "Place",
                     'name': "Beachfront aparte",
                     'description': "Heart of Lekki/V.I",
                     'number_rooms': 2,
                     'number_bathrooms': 2,
                     'amenity_ids': [str(uuid.uuid4())],
                     'updated_at': '{}'.format(c_ti.isoformat()),
                     'created_at': '{}'.format((c_ti - o_d).isoformat()),
                     'id': str(uuid.uuid4())
                     }
        p1 = Place(**cust_dict)
        self.assertEqual(p1.to_dict(), cust_dict)
        self.assertEqual(type(p1.updated_at), datetime.datetime)
        self.assertGreater(p1.updated_at, p1.created_at)
        self.assertEqual(p1.name, "Beachfront aparte")


class TestInstantiationArguments(unittest.TestCase):
    def testUsingArgsOnly(self):
        unused_id = str(uuid.uuid4())
        unused_date = datetime.datetime.now() - datetime.timedelta(days=1)
        p1 = Place("test", "kwargs", unused_id, unused_date)
        self.assertEqual(p1.to_dict(),
                         {'__class__': 'Place',
                          'updated_at': '{}'.format(p1.updated_at.isoformat()),
                          'created_at': '{}'.format(p1.created_at.isoformat()),
                          'id': p1.id})
        self.assertNotEqual(p1.id, unused_id)
        self.assertNotEqual(p1.updated_at, unused_date)

    def testUsingArgsAndKwargs(self):
        p1 = Place()
        p1_dict = p1.to_dict()

        p2 = Place("test", str(uuid.uuid4()),
                   datetime.datetime.now(), **p1_dict)
        self.assertEqual(p1_dict, p2.to_dict())
        self.assertEqual(p1.__dict__, p2.__dict__)
        self.assertIsNot(p1, p2)
