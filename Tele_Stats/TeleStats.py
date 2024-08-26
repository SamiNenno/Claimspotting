import os
import json
import argparse
from tqdm import tqdm
from pathlib import Path
from datetime import datetime, timedelta
from pymongo import MongoClient
from pymongo.server_api import ServerApi

PROJECT_DIRECTORY = str(Path(__file__).resolve().parent)

class TeleStats:
    """
    A class to collect and process statistics from a MongoDB database based on Telegram channel data.
    """

    def __init__(self, days_in_the_past: int = 0):
        """
        Initializes the TeleStats object.

        Parameters:
        - days_in_the_past (int): Number of days in the past to anchor the time for data processing. Defaults to 0 (today).
        """
        self.time_anchor = self.set_time_anchor(days_in_the_past=days_in_the_past)
        self.config = self.load_config()
        self.client = MongoClient(self.config["remote_mongo_dp_uri"], server_api=ServerApi('1'))
        self.db = self.client[self.config["mongo_db_name"]]
        self.stats_db = self.client[self.config["mongo_db_stats_name"]]
        self.global_template = self.load_template(collection_name="all_channels")
        self.query = self.load_query()

    def set_time_anchor(self, days_in_the_past: int):
        """
        Sets the time anchor based on the number of days in the past.

        Parameters:
        - days_in_the_past (int): Number of days in the past to set the anchor time.

        Returns:
        - datetime: The anchored datetime object.
        """
        if days_in_the_past == 0:
            time_anchor = datetime.now()
        else:
            today = datetime.today()
            time_anchor = today - timedelta(days=days_in_the_past)
            time_anchor = datetime.combine(time_anchor, datetime.min.time()) 
        return time_anchor

    def load_config(self):
        """
        Loads the configuration from a JSON file.

        Returns:
        - dict: Configuration dictionary loaded from the JSON file.
        """
        with open(os.path.join(PROJECT_DIRECTORY, "config.json"), "r", encoding='utf-8') as file:
            config = json.load(file)
        return config

    def load_query(self):
        """
        Creates a MongoDB query to fetch documents based on the anchored time.

        Returns:
        - dict: A MongoDB query dictionary to fetch documents within a specific date range.
        """
        start = datetime.combine(self.time_anchor.date(), datetime.min.time())
        end = start + timedelta(days=1)
        query = {
            'Publishing_datetime': {
                '$gte': start,
                '$lt': end
            }
        }
        return query

    def load_template(self, collection_name: str):
        """
        Loads a template JSON file and updates it with the current time and collection name.

        Parameters:
        - collection_name (str): The name of the collection to update in the template.

        Returns:
        - dict: The updated template dictionary.
        """
        with open(os.path.join(PROJECT_DIRECTORY, "template.json"), "r", encoding='utf-8') as file:
            template = json.load(file)
        template["Access_datetime"] = self.time_anchor
        template["data"]["Publishing_date"] = datetime.combine(self.time_anchor.date(), datetime.min.time())  
        template["Channel_Name"] = collection_name
        return template

    def load_todays_documents(self, collection_name: str):
        """
        Fetches documents from the specified collection that match the current query.

        Parameters:
        - collection_name (str): The name of the collection to fetch documents from.

        Returns:
        - pymongo.cursor.Cursor: A cursor to iterate over the documents in the collection.
        """
        collection = self.db[collection_name]
        documents = collection.find(self.query)
        return documents

    def update_global_template(self, template: dict):
        """
        Updates the global template with counts from a single collection's template.

        Parameters:
        - template (dict): A dictionary representing the template for a single collection.
        """
        for topic_name, count in template["data"]["Topic"].items():
            self.global_template["data"]["Topic"][topic_name] += count
        for narrative_name, count in template["data"]["Narratives"].items():
            self.global_template["data"]["Narratives"][narrative_name] += count

    def add_single_collection_stats(self, collection_name: str):
        """
        Processes a single collection's statistics and updates the template accordingly.

        Parameters:
        - collection_name (str): The name of the collection to process.

        Returns:
        - dict: The updated template dictionary for the collection.
        """
        template = self.load_template(collection_name=collection_name)
        documents = self.load_todays_documents(collection_name=collection_name)
        for doc in documents:
            topic = doc.get("Topic")
            narrative = doc.get("Narratives")
            if topic is not None:
                template["data"]["Topic"][topic] += 1
            if narrative is not None:
                narrative = narrative.replace("gerodet", "gerohdet")
                template["data"]["Narratives"][narrative] += 1
        self.update_global_template(template=template)
        return template

    def upload_template(self, template: dict, collection_name: str):
        """
        Uploads the processed template to the statistics database.

        Parameters:
        - template (dict): The template dictionary to upload.
        - collection_name (str): The name of the collection where the template will be uploaded.
        """
        collection = self.stats_db[collection_name]
        collection.insert_one(template)

    def add_stats(self):
        """
        Iterates over all collections in the database, processes their statistics, 
        and uploads the results to the statistics database.
        """
        collection_names = [collection_name for collection_name in self.db.list_collection_names() if collection_name != "all_channels"]
        for collection_name in tqdm(collection_names, total=len(collection_names), leave=False):
            template = self.add_single_collection_stats(collection_name=collection_name)
            self.upload_template(template=template, collection_name=collection_name)
        self.upload_template(template=self.global_template, collection_name="all_channels")

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--days_in_the_past', 
        type=int, 
        default=0, 
        help='Number of days in the past to get aggregations. Default is 0 (today).'
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    TeleStats(days_in_the_past=args.days_in_the_past).add_stats()