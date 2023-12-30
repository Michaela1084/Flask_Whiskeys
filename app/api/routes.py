from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Whiskey, Whiskey_schema, Whiskeys_schema

api = Blueprint('api',__name__, url_prefix='/api')

# @api.route('/getdata')
# def getdata():
#     return {'yee': 'haw'}

@api.route('/whiskey', methods = ['POST'])
@token_required
def create_whiskey(current_user_token):
    name = request.json['name']
    age = request.json['age']
    a_content = request.json['a_content']
    color = request.json['color']
    flavor = request.json['flavor']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    whiskey = Whiskey(name, age, a_content, color, flavor, user_token=user_token)

    db.session.add(whiskey)
    db.session.commit()

    response = Whiskey_schema.dump(whiskey)
    return jsonify(response)

@api.route('/whiskey', methods = ['GET'])
@token_required
def get_whiskey(current_user_token):
    a_user = current_user_token.token
    whiskeys = Whiskey.query.filter_by(user_token = a_user).all()
    response = Whiskeys_schema.dump(whiskeys)
    return jsonify(response)

# Optional! Might not work 
@api.route('/whiskey/<id>', methods = ['GET'])
@token_required
def get_single_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    response = Whiskey_schema.dump(whiskey)
    return jsonify(response)


#Updating
@api.route('/whiskey/<id>', methods = ['POST', 'PUT'])
@token_required
def update_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    whiskey.name = request.json['name']
    whiskey.age = request.json['age']
    whiskey.a_content = request.json['a_content']
    whiskey.color = request.json['color']
    whiskey.flavor = request.json['flavor']
    whiskey.user_token = current_user_token.token 

    db.session.commit()
    response = Whiskey_schema.dump(whiskey)
    return jsonify(response)


#Delete Endpoint
@api.route('/whiskey/<id>', methods = ['DELETE'])
@token_required
def delete_whiskey(current_user_token, id):
    whiskey = Whiskey.query.get(id)
    db.session.delete(whiskey)
    db.session.commit()
    response = Whiskey_schema.dump(whiskey)
    return jsonify(response)
