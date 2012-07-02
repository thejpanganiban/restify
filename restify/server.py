from flask import Flask, request, jsonify, abort
from pymongo import Connection
from werkzeug import exceptions
import simplejson as json

from classes import RestifyObject, RestifyCollection


app = Flask(__name__)
db_name = 'restify'
db = Connection()


@app.route('/')
def index():
    return "Restify"


@app.route('/classes')
def api_classes():
    return jsonify({
        'result': db[db_name].collection_names()
    })


@app.route('/classes/<class_name>', methods=['GET', 'POST'])
def api_collection(class_name):

    if request.method == 'GET':
        query_object = request.args.get('where')
        if query_object:
            try:
                query_object = json.loads(query_object)
            except Exception, e:
                return exceptions.BadRequest(e)
            collection = RestifyCollection.query(
                db, db_name, class_name, spec=query_object)
        else:
            collection = RestifyCollection.query(db, db_name, class_name)
            return jsonify(collection.to_dict())
    elif request.method == 'POST':
        if request.json.get('createdAt'):
            return exceptions.BadRequest('createdAt is a reserved keyword')
        if request.json.get('updatedAt'):
            return exceptions.BadRequest('updatedAt is a reserved keyword')
        obj = RestifyObject.create(db, db_name, class_name, request.json)
        return jsonify(obj.to_dict())
    else:
        return abort(405)


@app.route('/classes/<class_name>/<object_id>', methods=['GET', 'PUT', 'DELETE'])
def api_object(class_name, object_id):

    obj = RestifyObject.get_by_id(db, db_name, class_name, object_id)

    if obj:
        if request.method == 'GET':
            return jsonify(obj.to_dict())
        elif request.method == 'PUT':
            obj.update(request.json)
            return jsonify(obj.to_dict())
        elif request.method == 'DELETE':
            obj.delete()
            return ''
        else:
            return abort(405)
    else:
        return abort(404)


def debug():
    app.run(debug=True, host='0.0.0.0', port=52000)


if __name__ == '__main__':
    debug()
