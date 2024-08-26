import os
import json
from glob import glob
from tqdm import tqdm
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from Utils import load_config, get_most_recent_subfolders

class MatchUploader():
    """
    A class to handle the uploading of sibling match data to a MongoDB database.
    
    Attributes:
    ----------
    config : dict
        Configuration data loaded from an external source.
    client : pymongo.MongoClient
        MongoDB client for interacting with the database.
    db : pymongo.database.Database
        The specific database within MongoDB to store the documents.
    folder_dct : dict
        A dictionary of the most recent subfolders, presumably containing the data to upload.
    """
    
    def __init__(self) -> None:
        """
        Initializes the MatchUploader with configuration data and connects to MongoDB.
        """
        self.config = load_config()
        self.client = MongoClient(self.config["mongo_db"]["remote_mongo_dp_uri"], server_api=ServerApi('1'))
        self.db = self.client[self.config["mongo_db"]["mongo_db_name"]]
        self.folder_dct = get_most_recent_subfolders()
    
    def tag_parser(self, tagged_doc: dict) -> tuple:
        """
        Parses the tagged document to extract the ID and relevant sibling match data.
        
        Parameters:
        ----------
        tagged_doc : dict
            The dictionary representing the tagged document to be parsed.
        
        Returns:
        -------
        tuple
            A tuple containing the document ID and the new sibling data to update in the MongoDB collection.
        """
        _id = tagged_doc["_id"]
        new_data = {"$set": 
            {
            "Siblings": tagged_doc["Siblings"],
            }
        }
        return _id, new_data
    
    def tag_loader(self, collection_name: str, collection_path: str):
        """
        Loads JSON files from the specified collection path, parses each tagged document, and yields the necessary data.
        
        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection where the data will be uploaded.
        collection_path : str
            The path to the directory containing the JSON files to be loaded.
        
        Yields:
        ------
        tuple
            A tuple containing the document ID and the new sibling data to update in the MongoDB collection.
        """
        path_list = glob(os.path.join(collection_path, "*.json"))
        for path in tqdm(path_list, total=len(path_list), desc=collection_name, leave=False):
            with open(path, "r") as f:
                tagged_doc = json.load(f)
            _id, new_data = self.tag_parser(tagged_doc=tagged_doc)
            yield _id, new_data
    
    def upload_collection(self, collection_name: str, collection_path: str) -> None:
        """
        Updates a MongoDB collection with sibling match data parsed from JSON files in the specified directory.
        
        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to update.
        collection_path : str
            The path to the directory containing the JSON files to be uploaded.
        """
        collection = self.db[collection_name]
        for _id, new_data in self.tag_loader(collection_name=collection_name, collection_path=collection_path):
            query = {"_id": ObjectId(_id)}
            collection.update_one(query, new_data)
    
    def upload(self) -> None:
        """
        Iterates through all collections and uploads the corresponding sibling data from the most recent subfolders.
        """
        for collection_name, collection_path in tqdm(self.folder_dct.items(), total=len(self.folder_dct), desc="Upload siblings", leave=False):
            self.upload_collection(collection_name=collection_name, collection_path=collection_path)

if __name__ == "__main__":
    MatchUploader().upload()
