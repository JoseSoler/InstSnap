#!flask/bin/python
from flask import Flask, jsonify, request
from repositories.postRepository import PostRepository
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # https://flask-cors.readthedocs.io/en/latest/

repository = PostRepository('mongodb://localhost:27017/')


# TODO: Find out how to use a proper logger instead of using print

@app.route('/api')
def index():
    """
    Offers the list of resources this API manages
    :return: The list of resources in json format
    """
    return jsonify({'instSnap:posts': '/api/posts'})


@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = repository.find_all()
    print("Serializing {} post(s)".format(len(posts)))
    return jsonify(posts)


@app.route('/api/posts/<string:post_id>', methods=['GET'])
def get_post(post_id):
    post = repository.find_by_id(post_id)
    return jsonify(post.to_dictionary())


@app.route('/api/posts/_search', methods=['POST'])
def search_posts():
    query = request.get_json()
    posts = repository.find_by_query(query)
    print("Serializing {} post(s)".format(len(posts)))
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)
