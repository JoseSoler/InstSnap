#!flask/bin/python
from flask import Flask, jsonify, request
from repositories.postRepository import PostRepository
from flask_cors import CORS

app = Flask(__name__)

# CORS must be allowed if the server that serves angular app
# is not the same as the server offering the REST API
# https://flask-cors.readthedocs.io/en/latest/
CORS(app)

# TODO: Find out how to use a proper logger instead of using print
# TODO: Externalise connection string to a properties file
repository = PostRepository('mongodb://localhost:27017/')


@app.route('/api')
def index():
    """
    Offers the list of resources this API manages
    :return: The list of resources in json format
    """
    return jsonify({'instSnap:posts': '/api/posts'})


@app.route('/api/posts', methods=['GET'])
def get_posts():
    """
    :return: All the posts in database (very risky in terms of memory consumption)
    """
    posts = repository.find_all()
    print("Serializing {} post(s)".format(len(posts)))
    return jsonify(posts)


@app.route('/api/posts/<string:post_id>', methods=['GET'])
def get_post(post_id):
    """
    :param post_id: The id of the Post to be retrieved from database
    :return: Whether the Post or 404 not found
    """
    post = repository.find_by_id(post_id)
    return jsonify(post.to_dictionary())


@app.route('/api/posts/_search', methods=['POST'])
def search_posts():
    """
    Searches for posts based on the user's inquiry
    :return: The list of Posts that matches the inquiry
    """
    user_inquiry = request.get_json()
    posts = repository.find_by_query(user_inquiry)
    print("Serializing {} post(s)".format(len(posts)))
    return jsonify(posts)


if __name__ == '__main__':
    app.run(debug=True)
