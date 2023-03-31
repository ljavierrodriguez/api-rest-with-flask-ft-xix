from datetime import datetime
from slugify import slugify
from models import Post, Tag
from flask import Blueprint, request, jsonify

bpPost = Blueprint('bpPost', __name__)

@bpPost.route('/posts', methods=['GET', 'POST'])
@bpPost.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def posts(id = None):

    if request.method == 'GET':


        if id is not None:
            post = Post.query.get(id)

            if not post:
                return jsonify({ "status": 404, "message": "Article Not Found!"}), 404

            return jsonify(post.serialize()), 200

        else:
            posts = Post.query.all()
            posts = list(map(lambda post: post.serialize(), posts))

            return jsonify(posts), 200


    if request.method == 'POST':
        
        title = request.json.get('title')
        content = request.json.get('content')
        date = request.json.get('date', datetime.now())
        is_published = request.json.get('is_published', False)
        users_id = request.json.get('users_id')
        info_tags = request.json.get('tags')

        

        post = Post()
        post.title = title
        post.slug = slugify(title, '-')
        post.content = content
        post.is_published = is_published
        post.users_id = users_id

        if info_tags and len(info_tags) > 0:
            for tag_id in info_tags:
                tag = Tag.query.get(tag_id)
                post.tags.append(tag)

        post.save()

        return jsonify({ "status": 201, "message": "Article created successfully", "article": post.serialize()}), 201

    if request.method == 'PUT':
        
        title = request.json.get('title')
        content = request.json.get('content')
        date = request.json.get('date', datetime.now())
        is_published = request.json.get('is_published', False)
        users_id = request.json.get('users_id')

        post = Post.query.get(id)

        if not post:
            return jsonify({ "status": 404, "message": "Article Not Found" }), 404

        post.title = title
        post.slug = slugify(title, '-')
        post.content = content
        post.is_published = is_published
        post.users_id = users_id
        post.save()

        return jsonify({ "status": 201, "message": "Article created successfully", "article": post.serialize()}), 201