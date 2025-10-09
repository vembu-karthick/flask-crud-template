from flask import Flask, request, jsonify
from waitress import serve
from flask_pymongo import PyMongo
import bcrypt
from jwt import (JWT, jwk_from_dict)
from jwt.utils import get_int_from_datetime
from datetime import datetime, timedelta, timezone
from bson.objectid import ObjectId
import json
from functools import wraps
import os

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb+srv://geerthikumar2100:sXjD2GhXx0SQJXj4@cluster0.d2krt.mongodb.net/?retryWrites=true&w=majority"
secret_key = jwk_from_dict(json.load(open('rsa_privkey.json')))

mongo = PyMongo(app)
mongo.db = mongo.cx['templates']
_jwt = JWT()

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = _jwt.decode(token, secret_key)
            current_user = mongo.db.users.find_one({'_id': ObjectId(data['user_id'])})
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorator

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if mongo.db.users.find_one({'email': data['email']}):
            return jsonify({'message': 'User already exists'}), 400
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed_password
        }
        mongo.db.users.insert_one(user_data)
        return jsonify({'message': 'User registered successfully!'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = mongo.db.users.find_one({'email': data['email']})
        if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        token = _jwt.encode(payload={'user_id': str(user['_id']), 'exp': get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=1))}, 
                            key=secret_key, alg='RS256')
        return jsonify({'token': token}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template', methods=['POST'])
@token_required
def insert_template(current_user):
    try:
        data = request.get_json()
        template_data = {
            'template_name': data['template_name'],
            'subject': data['subject'],
            'body': data['body'],
            'user_id': ObjectId(current_user['_id'])
        }
        result = mongo.db.templates.insert_one(template_data)
        template_id = str(result.inserted_id)
        return jsonify({'message': 'Template created successfully!', 'Template ID': template_id}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template', methods=['GET'])
@token_required
def get_all_templates(current_user):
    try:
        templates = mongo.db.templates.find({'user_id': ObjectId(current_user['_id'])})
        templates_list = []
        for template in templates:
            template_data = {
                'template_name': template['template_name'],
                'subject': template['subject'],
                'body': template['body'],
                'template_id': str(template['_id'])
            }
            templates_list.append(template_data)
        return jsonify({'templates': templates_list}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template/<template_id>', methods=['GET'])
@token_required
def get_single_template(current_user, template_id):
    try:
        template = mongo.db.templates.find_one({'_id': ObjectId(template_id), 'user_id': ObjectId(current_user['_id'])})
        if not template:
            return jsonify({'message': 'Template not found'}), 404
        template_data = {
            'template_name': template['template_name'],
            'subject': template['subject'],
            'body': template['body']
        }
        return jsonify({'template': template_data}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template/<template_id>', methods=['PUT'])
@token_required
def update_template(current_user, template_id):
    try:
        data = request.get_json()
        template = mongo.db.templates.find_one({'_id': ObjectId(template_id), 'user_id': ObjectId(current_user['_id'])})
        if not template:
            return jsonify({'message': 'Template not found'}), 404
        updated_template = {
            'template_name': data['template_name'],
            'subject': data['subject'],
            'body': data['body']
        }
        mongo.db.templates.update_one({'_id': ObjectId(template_id)}, {'$set': updated_template})
        return jsonify({'message': 'Template updated successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template/<template_id>', methods=['DELETE'])
@token_required
def delete_template(current_user, template_id):
    try:
        template = mongo.db.templates.find_one({'_id': ObjectId(template_id), 'user_id': ObjectId(current_user['_id'])})
        if not template:
            return jsonify({'message': 'Template not found'}), 404
        mongo.db.templates.delete_one({'_id': ObjectId(template_id)})
        return jsonify({'message': 'Template deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/template/<template_id>', methods=['PATCH'])
@token_required
def patch_template(current_user, template_id):  # Renamed function
    try:
        data = request.get_json()
        update_fields = {}

        if 'template_name' in data:
            update_fields['template_name'] = data['template_name']
        if 'subject' in data:
            update_fields['subject'] = data['subject']
        if 'body' in data:
            update_fields['body'] = data['body']

        if not update_fields:
            return jsonify({'message': 'No fields provided for update'}), 400

        result = mongo.db.templates.update_one(
            {'_id': ObjectId(template_id), 'user_id': ObjectId(current_user['_id'])},
            {'$set': update_fields}
        )

        if result.matched_count == 0:
            return jsonify({'message': 'Template not found or unauthorized'}), 404

        return jsonify({'message': 'Template updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 500


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
