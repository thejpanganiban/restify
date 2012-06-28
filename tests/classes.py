from pymongo import Connection
from restify.classes import RestifyObject
from bson.objectid import ObjectId
import unittest


class RestifyObjectTestCase(unittest.TestCase):

  def setUp(self):
    self.connection = Connection()
    self.database_name = 'classtest'
    self.collection_name = 'restifyobject'
    self.fixture_data = {'name': "Jesse",
                         'age': 21,
                        }
    self.plenty_fixture_data = [
          {'name': "Jesse", 'age': 21},
          {'name': "Mikko", 'age': 20},
          {'name': "Jhelo", 'age': 21},
        ]

  def tearDown(self):
    self.connection.drop_database(self.database_name)
    self.connection = None

  def test_create(self):
    """Test creation of restify object."""
    r = RestifyObject.create(self.connection, self.database_name,
                             self.collection_name, self.fixture_data)
    self.assertTrue(r)

  def test_created_attributes(self):
    """Test created restify object attributes."""
    r = RestifyObject.create(self.connection, self.database_name,
                             self.collection_name, self.fixture_data)
    self.assertTrue(hasattr(r, 'createdAt'))
    self.assertTrue(hasattr(r, 'id'))
    self.assertTrue(hasattr(r, 'name'))
    self.assertTrue(hasattr(r, 'age'))



  def test_to_dict(self):
    """Test to_dict bound method."""
    r = RestifyObject.create(self.connection, self.database_name,
                             self.collection_name, self.fixture_data)
    self.assertTrue(isinstance(r.to_dict(), dict))
    self.assertEqual(r.to_dict()['name'], self.fixture_data['name'])
    self.assertEqual(r.to_dict()['age'], self.fixture_data['age'])

  def test_get_by_id(self):
    objs = []
    for fixture_data in self.plenty_fixture_data:
      r = RestifyObject.create(self.connection, self.database_name,
                               self.collection_name, fixture_data)
      objs.append(r)
    obj = RestifyObject.get_by_id(self.connection, self.database_name,
                                     self.collection_name, objs[0].id)
    self.assertTrue(obj)
    self.assertEqual(obj.to_dict(), objs[0].to_dict())

    obj = RestifyObject.get_by_id(self.connection, self.database_name,
                                  self.collection_name, ObjectId())
    self.assertFalse(obj)


if __name__ == '__main__':
  unittest.main()
