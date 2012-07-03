Restify
=======

A Mongodb RESTful interface

Requirements
------------

* Mongodb
* Python
* flask
* pymongo

Usage
-----

Querying:

    curl -X GET \
         <host>/<engine_name>/classes/<class_name>

or

    curl -X GET \
         <host>/<engine_name>/classes/<class_name>?where=<mongodb_query>

example mongodb query

    curl -X GET \
         <host>/<engine_name>/classes/<class_name>?where={'name': 'Jesse'}


Creating objects:

    curl -X POST \
         -H "Content-Type: application/json" \
         -d '{"name": "Jesse", "age": 21}' \
         <host>/<engine_name>/classes/<class_name>


Updating objects:

    curl -X PUT \
         -H "Content-Type: application/json" \
         -d '{"name": "Jesse Panganiban"}' \
         <host>/<engine_name>/classes/<class_name>/<object_id>


Deleting objects:

    curl -X DELETE \
         <host>/<engine_name>/classes/<class_name>/<object_id>


See http://www.mongodb.org for queries and updating objects (modifiers).



TODO
----

Here's a list of things to do. Fork me! :)

* Authentication
* ACL (Access Control List)
* Controller Tests
* Multiple DBs in single instance
* Use gevent.pywsgi (Check if pymongo is gevent safe)
