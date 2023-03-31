from models import User, Profile
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

bpUser = Blueprint('bpUser', __name__)

@bpUser.route('/users', methods=['GET'])
def all_users():

    users = User.query.all()  # [<User 1>, <User 2>]
    users = list(map(lambda user: user.serialize_with_profile(), users))

    return jsonify(users), 200

@bpUser.route('/users', methods=['POST'])
def create_user():

    name = request.json.get('name', "")
    email = request.json.get('email')
    password = request.json.get('password')

    biography = request.json.get('biography')
    facebook = request.json.get('facebook')


    if not email:
        return jsonify({"status": 400, "message": "Email is required"}), 400

    if not password:
        return jsonify({"status": 400, "message": "Password is required"}), 400

    found = User.query.filter_by(email=email).first()

    if found:
        return jsonify({"status": 400, "message": "Email already exists"}), 400


    profile = Profile()
    profile.biography = biography
    profile.facebook = facebook

    user = User()
    user.name = name
    user.email = email
    user.password = generate_password_hash(password)

    user.profile = profile

    user.save()

    #profile.users_id = user.id
    #profile.save()

    return jsonify({"status": 200, "message": "User created successfully", "user": user.serialize()}), 201

@bpUser.route('/users/<int:id>', methods=['PUT'])
def update_user(id):

    name = request.json.get('name', "")
    email = request.json.get('email')
    password = request.json.get('password')


    biography = request.json.get('biography')
    facebook = request.json.get('facebook')

    if email:
        found = User.query.filter_by(email=email).first()
        if found.id != id:
            return jsonify({"status": 400, "message": "Email already exists"}), 400

    user = User.query.get(id)

    if not user:
        return jsonify({"status": 404, "message": "User not found"}), 404

    user.name = name if name else user.name
    user.email = email if email else user.email
    user.password = generate_password_hash(password) if password  else user.password

    user.profile.biography = biography
    user.profile.facebook = facebook

    user.update()

    #profile = Profile.query.filter_by(users_id=id).first()
    #profile.biography = biography
    #profile.facebook = facebook
    #profile.update()

    return jsonify({"status": 200, "message": "User created successfully", "user": user.serialize()}), 201

@bpUser.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):

    user = User.query.get(id)

    if not user:
        return jsonify({"status": 404, "message": "User not found"}), 404

    user.delete()
    
    return jsonify({"status": 200, "message": "User deleted successfully", "user": {}}), 200