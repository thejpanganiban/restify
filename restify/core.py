from werkzeug import exceptions
import simplejson as json
from flask import Flask, request, jsonify, abort

from .engines import get_engine_or_fail


app = Flask(__name__)


@app.route('/')
def index():
    return "Restify"


@app.route('/<engine_name>/classes/', methods=['GET'])
def api_classes(engine_name):
    is_engine, engine = get_engine_or_fail(engine_name)
    if is_engine:
        return jsonify({'result': engine.list_collections()})
    return exceptions.BadRequest(engine)


@app.route('/<engine_name>/classes/<class_name>/', methods=['GET', 'POST'])
def api_collection(engine_name, class_name):
    is_engine, engine = get_engine_or_fail(engine_name)
    if not is_engine:
        return exceptions.BadRequest(engine)
    if request.method == 'GET':
        query = request.args.get('where')
        if query:
            try:
                query = json.loads(query)
            except Exception, e:
                return exceptions.BadRequest(e)
            return jsonify({'result': engine.query_collection(class_name, query)})
        else:
            return jsonify({'result': engine.query_collection(class_name)})
    elif request.method == 'POST':
        if request.json.get('createdAt'):
            return exceptions.BadRequest('createdAt is a reserved keyword')
        if request.json.get('updatedAt'):
            return exceptions.BadRequest('updatedAt is a reserved keyword')
        new_obj = engine.create(class_name, request.json)
        return jsonify(new_obj.to_dict())
    else:
        return abort(405)


@app.route('/<engine_name>/classes/<class_name>/<object_id>',
    methods=['GET', 'PUT', 'DELETE'])
def api_object(engine_name, class_name, object_id):
    is_engine, engine = get_engine_or_fail(engine_name)
    if not is_engine:
        return exceptions.BadRequest(engine)
    obj = engine.get_by_id(class_name, object_id)
    if obj:
        if request.method == 'GET':
            return jsonify(obj.to_dict())
        elif request.method == 'PUT':
            obj = engine.update(class_name, request.json, object_id)
            return jsonify(obj.to_dict())
        elif request.method == 'DELETE':
            obj.delete()
            return ''
        else:
            return abort(405)
    else:
        return abort(404)
