from pymongo import Connection
from restify.classes import RestifyObject, RestifyCollection
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
    """Test get_by_id method."""
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

  def test_delete(self):
    """Test delete method."""
    r = RestifyObject.create(self.connection, self.database_name,
                             self.collection_name, self.fixture_data)
    obj_id = r.id
    r.delete(self.connection, self.database_name, self.collection_name)
    deleted_obj = RestifyObject.get_by_id(self.connection, self.database_name,
                                          self.collection_name, obj_id)
    self.assertFalse(deleted_obj)

  def test_update(self):
    """Test update method."""
    r = RestifyObject.create(self.connection, self.database_name,
                             self.collection_name, self.fixture_data)
    # To use $inc modifier
    r.update(self.connection, self.database_name, self.collection_name,
             {'$inc': { 'age': 1 }})
    self.assertEqual(r.age, self.fixture_data['age'] + 1)

    # To use $set modifier (possible conflict with updatedAt)
    new_name = 'new Jesse'
    r.update(self.connection, self.database_name, self.collection_name,
             {'$set': {'name': new_name}})
    self.assertEqual(r.name, new_name)
    self.assertTrue(r.updatedAt)

    # and again just for the kicks
    new_name = 'and Jesse'
    r.update(self.connection, self.database_name, self.collection_name,
             {'$set': {'name': new_name}})
    self.assertEqual(r.name, new_name)
    self.assertTrue(r.updatedAt)



class RestifyCollectionTestCase(unittest.TestCase):

  def setUp(self):
    self.connection = Connection()
    self.database_name = 'classtest'
    self.collection_name = 'restifycollection'
    self.plenty_fixture_data = [
          {'name': "Jesse", 'age': 21},
          {'name': "Mikko", 'age': 20},
          {'name': "Jhelo", 'age': 21},
        ]
    self.plenty_fixture_objects = []
    for fixture_data in self.plenty_fixture_data:
      obj = RestifyObject.create(self.connection, self.database_name,
                                 self.collection_name, fixture_data)
      self.plenty_fixture_objects.append(obj)

  def tearDown(self):
    self.connection.drop_database(self.database_name)
    self.connection = None

  def test_query(self):
    """Test query method."""
    c = RestifyCollection.query(self.connection, self.database_name,
                                self.collection_name)
    self.assertTrue(c)

    aq = RestifyCollection.query(self.connection, self.database_name,
                                 self.collection_name, spec={'name': "Jesse"})
    self.assertEqual(aq.result[0].age, 21)
    self.assertEqual(aq.result[0].name, "Jesse")
    self.assertEqual(len(aq.result), 1)

  def test_to_dict(self):
    """Test to_dict method."""
    c = RestifyCollection.query(self.connection, self.database_name,
                                self.collection_name)
    self.assertTrue(c)
    fixture_result_dict = {
          'result': [obj.to_dict() for obj in self.plenty_fixture_objects]
        }
    self.assertTrue(c.to_dict(), fixture_result_dict)


if __name__ == '__main__':
  unittest.main()
