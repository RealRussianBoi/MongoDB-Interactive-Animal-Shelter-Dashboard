import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

class AnimalShelter:
    """CRUD operations for the Animal collection in MongoDB"""

    def __init__(self, username, password):
        """
        Initialize the MongoDB connection using user-provided credentials.
        """
        try:
            # Get environment variables for host and port
            host = os.getenv('MONGO_HOST', 'nv-desktop-services.apporto.com')
            port = int(os.getenv('MONGO_PORT', 32995))

            # Construct the MongoDB URI using the provided username and password
            mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"

            # Connect to MongoDB
            self.client = MongoClient(mongo_uri)
            self.database = self.client["AAC"]
            self.collection = self.database["animals"]

            print("Connected to MongoDB successfully!")

        except PyMongoError as e:
            raise Exception(f"Failed to connect to MongoDB: {e}")

    def create(self, data):
        """Insert a document into the animals collection."""
        if data is not None and isinstance(data, dict):
            try:
                result = self.collection.insert_one(data)
                return True if result.inserted_id else False
            except PyMongoError as e:
                print(f"Error inserting document: {e}")
                return False
        else:
            raise ValueError("Data must be a non-empty dictionary.")

    def read(self, query):
        """Query documents from the animals collection."""
        if query is not None and isinstance(query, dict):
            try:
                cursor = self.collection.find(query)
                return list(cursor)
            except PyMongoError as e:
                print(f"Error querying documents: {e}")
                return []
        else:
            raise ValueError("Query must be a dictionary.")

    def update(self, query, new_data, update_many=False):
        """
        Update document(s) in the animals collection.
        
        :param query: A dictionary representing the filter criteria.
        :param new_data: A dictionary representing the data to update.
        :param update_many: Boolean indicating if multiple documents should be updated.
        :return: The number of documents modified.
        """
        if query is None or not isinstance(query, dict):
            raise ValueError("Query must be a non-empty dictionary.")
        if new_data is None or not isinstance(new_data, dict):
            raise ValueError("New data must be a non-empty dictionary.")
        
        try:
            update = {"$set": new_data}
            if update_many:
                result = self.collection.update_many(query, update)
            else:
                result = self.collection.update_one(query, update)
            return result.modified_count
        except PyMongoError as e:
            print(f"Error updating documents: {e}")
            return 0

    def delete(self, query, delete_many=False):
        """
        Delete document(s) from the animals collection.
        
        :param query: A dictionary representing the filter criteria.
        :param delete_many: Boolean indicating if multiple documents should be deleted.
        :return: The number of documents deleted.
        """
        if query is None or not isinstance(query, dict):
            raise ValueError("Query must be a non-empty dictionary.")

        try:
            if delete_many:
                result = self.collection.delete_many(query)
            else:
                result = self.collection.delete_one(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Error deleting documents: {e}")
            return 0