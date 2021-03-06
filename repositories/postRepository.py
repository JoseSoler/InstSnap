from pymongo import MongoClient
from datetime import datetime
import re


class PostRepository:
    """
     A Repository abstraction (based on DDD practises) that
     handles possible actions with a Post entity against
     the database

    """

    def __init__(self, connection_url):
        self.client = MongoClient(connection_url)
        self.posts_collection = self.client.instSnap.posts

    def __del__(self):
        self.client.close()

    def find_all(self):
        """
        Finds all post documents within database

        Notice please the risky approach here as we are loading all existing documents into memory.
        A "real world" approach would be to implement Pagination

        :return: A list of all Post Objects persisted in the repository as documents
        """
        cursor = self.posts_collection.find()

        return [document for document in cursor]

    def find_by_id(self, post_id):
        """
        Finds a Post based on the passed id

        :param post_id: The id of the post

        :return: The found post document or None if it wasn't found
        """
        return self.posts_collection.find_one({"_id": post_id})

    def find_by_query(self, inquiry):
        """
        Method that knows how to map an inquiry from the client to a query in MongoDB

        NOTE: If the queries were more complex, this method should be split in more specialized
              methods or classes

        :param inquiry: A dictionary containing the query description from the Client
        :return: The post documents that matches the search criteria
        """
        query = {}
        projection = {}

        # Let's build the query
        if "user_id" in inquiry and inquiry['user_id']:
            query['user_id'] = int(inquiry['user_id'])

        if "text" in inquiry and inquiry['text']:
            regex = re.compile(inquiry['text'], re.IGNORECASE)
            query['text'] = {"$regex": regex}

        if "start_time" in inquiry and "end_time" in inquiry:
            if inquiry['start_time'] and inquiry['end_time']:
                query['created_at'] = {"$gte": datetime.fromisoformat(inquiry['start_time'])}
                query['expires_at'] = {"$lte": datetime.fromisoformat(inquiry['end_time'])}

        elif "start_time" in inquiry and inquiry['start_time']:
            query['created_at'] = {"$gte": datetime.fromisoformat(inquiry['start_time'])}

        elif "end_time" in inquiry and inquiry['end_time']:
            query['expires_at'] = {"$lte": datetime.fromisoformat(inquiry['end_time'])}

        # Let's build the projection
        if "search_fields" in inquiry and inquiry["search_fields"]:
            projection["_id"] = 0  # Just hides _id

            for field in inquiry["search_fields"].split():
                projection[str(field)] = 1

        # Deciding which query should be executed
        if query and projection:
            print("Going to run the following query {} with projection {}".format(query, projection))
            cursor = self.posts_collection.find(query, projection)
        elif query:
            print("Going to run the following query {}".format(query))
            cursor = self.posts_collection.find(query)
        elif projection:
            print("No filters, only projection {}".format(projection))
            cursor = self.posts_collection.find({}, projection)
        else:
            print("No filters and No projection... returning all")
            return self.find_all()

        return [document for document in cursor]

    def save_one(self, post):
        """
        Persists the passed Post object into database

        :param post: The Post object

        :return: The id given by the database
        """
        return self.posts_collection.insert_one(post.to_dictionary()).inserted_id

    def save_all(self, posts):
        """
        Persists all the passed Post objects into database

        :param posts: The list of Post objects

        :return: Nothing

        """
        for post in posts:
            self.posts_collection.insert_one(post.to_dictionary())
