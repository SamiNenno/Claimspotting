import os
import json
import shutil
import datetime
from tqdm import tqdm
from glob import glob
from pathlib import Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Telegram_API_Request import Telegram_Scraper
from concurrent.futures import ProcessPoolExecutor
NOW = datetime.datetime.now()
ONE_AND_A_HALF_HOURS_AGO = NOW - datetime.timedelta(hours=1.5) # Assumes that scraping is happening every 1.5 hours or less frequent, e.g. every 2 hours. Otherwise identical Telegram Posts get saved multiple times as seperate documents in MongoDB.
TWO_DAYS_AGO = NOW - datetime.timedelta(days=2)
TEN_DAYS_AGO = NOW - datetime.timedelta(days=10)

class TelegramMongoDB():
    """
    TelegramMongoDB class provides methods to interact with Telegram data and store it in MongoDB.

    This class includes methods to retrieve message paths, parse messages, save parsed messages,
    and manage the storage of results.

    Methods:
        get_result_path_list(result_name: str) -> list:
            Retrieves a list of paths to result files for a given result name.
        get_file_name(message: dict) -> tuple:
            Constructs the file name for a message and checks if it exists.
        message_iter(path: str) -> dict:
            Iterates over messages in a given file path and yields them as dictionaries.
        parse_new_message(message: dict) -> dict:
            Parses a new message to the required format with additional metadata.
        extract_appendix(message: dict, parsed_message: dict) -> dict:
            Extracts and constructs additional data (appendix) for an existing message.
        parse_message(message: dict, collection: pymongo.collection.Collection):
            Parses a message and updates or inserts it into the specified MongoDB collection.
        delete_oldest_folder(max_folders: int):
            Deletes the oldest folder in the results directory if the number of folders exceeds max_folders.
        parse_channel(path: str):
            Parses a channel's messages and stores them in the specified MongoDB database and collection.
        transfer_to_mongoDB(result_name: str, db_name: str, db_port: int, cores: int = 1, max_folders: int = 5):
            Transfers parsed messages to MongoDB, using multiple cores if specified, and manages the result folders.
    """
    def __init__(self) -> None:
        self.project_path = Path(Path(__file__).resolve().parent)
        self.session_counter = 0
        with open(self.make_path("Utils/config.json"), 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        with open(self.make_path("Utils/LowFrequencyChannels.txt"), 'r') as file:
            self.low_frequency_channels = file.readlines()
            
    def make_path(self, extension:str):
        return str(self.project_path / extension)
        
    def get_result_path_list(self, result_name):
        """
        Retrieves a list of paths to result files for a given result name.

        Args:
            result_name (str): The name of the result directory.

        Returns:
            list: A list of file paths matching the result name.
        """
        path = os.path.join(self.make_path("Results"), f"{result_name}/*.json")
        return glob(path)

    def get_file_name(self, message):
        """
        Constructs the file name for a message and checks if it exists.

        Args:
            message (dict): The message dictionary containing the 'Channel_Name' and 'Message_ID'.

        Returns:
            tuple: A tuple containing the file name and a boolean indicating if the file exists.
        """
        file_name = os.path.join(self.make_path("Parsed_Results"), message["Channel_Name"], f"{message['Message_ID']}.json")
        file_exists = os.path.exists(file_name)
        return file_name, file_exists

    def message_iter(self, path):
        """
        Iterates over messages in a given file path and yields them as dictionaries.

        Args:
            path (str): The path to the file containing messages.

        Yields:
            dict: A dictionary representing a message.
        """
        with open(path, 'r') as file:
            for line in file:
                try:
                    message = json.loads(line.strip())
                    yield message
                except json.JSONDecodeError:
                    continue

    def parse_new_message(self, message):
        """
        Parses a new message to the required format with additional metadata.

        Args:
            message (dict): The original message dictionary.

        Returns:
            dict: The parsed message dictionary with additional metadata.
        """
        parsed_message = dict()
        parsed_message["Message_ID"] = message["Message_ID"]
        parsed_message["User"] = message["User"]
        parsed_message["Channel_Name"] = message["Channel_Name"]
        parsed_message["Link"] = message["Link"]
        parsed_message["Publishing_datetime"] = message["Publishing_datetime"]
        parsed_message["Access_datetime"] = message["Access_datetime"]
        parsed_message["Edit_datetime"] = message["Edit_datetime"]
        parsed_message["Has_audio"] = message["Has_audio"]
        parsed_message["Has_document"] = message["Has_document"]
        parsed_message["Has_sticker"] = message["Has_sticker"]
        parsed_message["Has_animation"] = message["Has_animation"]
        parsed_message["Has_video"] = message["Has_video"]
        parsed_message["Member_count"] = [
            {
                "Access_datetime": message["Access_datetime"],
                "Member_count": message["Member_count"]
            }
        ]
        parsed_message["Content"] = [
            {
                "Access_datetime": message["Access_datetime"],
                "Is_edited": message["Edit_datetime"] is not None,
                "Edit_datetime": message["Edit_datetime"],
                "Text": message["Text"],
                "Caption": message["Caption"],
                "Entities": message["Entities"],
            }
        ]
        parsed_message["Engagement"] = [
            {
                "Access_datetime": message["Access_datetime"],
                "Views": message["Views"],
                "Forwards": message["Forwards"],
                "Reactions": message["Reactions"],
            }
        ]
        return parsed_message

    def extract_appendix(self, message, parsed_message):
        """
        Extracts and constructs additional data (appendix) for an existing message.

        Args:
            message (dict): The original message dictionary.
            parsed_message (dict): The already parsed message dictionary from the database.

        Returns:
            dict: The appendix dictionary containing additional Member_count, Engagement, and Content data.
        """
        appendix = dict(
            Member_count=[{
                "Access_datetime": message["Access_datetime"],
                "Member_count": message["Member_count"]
            }],
            Engagement=[{
                "Access_datetime": message["Access_datetime"],
                "Views": message["Views"],
                "Forwards": message["Forwards"],
                "Reactions": message["Reactions"],
            }]
        )
        if parsed_message["Content"][-1]["Is_edited"]:
            old_edit_time = parsed_message["Edit_datetime"]
            if message["Access_datetime"] is None:
                appendix["Content"] = None
            else:
                new_edit_time = message["Edit_datetime"]
                if old_edit_time != new_edit_time:
                    appendix["Content"] = [{
                        "Access_datetime": message["Access_datetime"],
                        "Is_edited": message["Edit_datetime"] is not None,
                        "Edit_datetime": message["Edit_datetime"],
                        "Text": message["Text"],
                        "Caption": message["Caption"],
                        "Entities": message["Entities"],
                    }]
                else:
                    appendix["Content"] = None
        elif message["Edit_datetime"] is not None:
            appendix["Content"] = [{
                "Access_datetime": message["Access_datetime"],
                "Is_edited": message["Edit_datetime"] is not None,
                "Edit_datetime": message["Edit_datetime"],
                "Text": message["Text"],
                "Caption": message["Caption"],
                "Entities": message["Entities"],
            }]
        else:
            appendix["Content"] = None
        return appendix

    def parse_message(self, message, collection):
        """
        Parses a message and updates or inserts it into the specified MongoDB collection.
        To reduce insertion costs for MongoDB, only insert Telegram posts within the last two days and ignore older ones.
        To reduce insertion costs for MongoDB, only check if Telegram posts exists already if it is older than 1.5 hours (assumes scraping period of no more than 1.5 hours)
        
        Args:
            message (dict): The original message dictionary.
            collection (pymongo.collection.Collection): The MongoDB collection to update or insert the message into.
        """
        def parse_datetime(datetime_str):
            if datetime_str and isinstance(datetime_str, str):
                try:
                    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
                except ValueError:
                    return None
            return None
        message["Publishing_datetime"] = parse_datetime(message["Publishing_datetime"])
        message["Access_datetime"] = parse_datetime(message["Access_datetime"])
        message["Edit_datetime"] = parse_datetime(message["Edit_datetime"])
        
        if  message["Publishing_datetime"] < TWO_DAYS_AGO:
            # if post is older than two days, don't add it to the collection
            return 
        elif ONE_AND_A_HALF_HOURS_AGO < message["Publishing_datetime"]:
            # if post was published within the last 1.5 hours, dont check if it already exists and just add it to the collection.
            collection.insert_one(self.parse_new_message(message=message))
        else:
            # if post is within the last two days but not within the last 1.5 hours, check if it already exists and only if not add a new document, otherwise append it to existing document.
            query = {
                "Message_ID": message["Message_ID"],
            }
            parsed_message = collection.find_one(query)
            if parsed_message:
                appendix = self.extract_appendix(message, parsed_message)
                collection.update_one(
                    {"Message_ID": message["Message_ID"]},
                    {"$push": {"Member_count": {"$each": appendix["Member_count"]}}}
                )
                collection.update_one(
                    {"Message_ID": message["Message_ID"]},
                    {"$push": {"Engagement": {"$each": appendix["Engagement"]}}}
                )
                if appendix["Content"] is not None:
                    collection.update_one(
                        {"Message_ID": message["Message_ID"]},
                        {"$push": {"Content": {"$each": appendix["Content"]}}}
                    )
            else:
                collection.insert_one(self.parse_new_message(message=message))

    def delete_oldest_folder(self, max_folders):
        """
        Deletes the oldest folder in the results directory if the number of folders exceeds max_folders.

        Args:
            max_folders (int): The maximum number of folders to keep.
        """
        results_path = self.make_path("Results")
        folders = [f for f in os.listdir(results_path) if os.path.isdir(os.path.join(results_path, f))]
        if len(folders) <= max_folders:
            return

        def parse_folder_datetime(folder_name):
            try:
                return datetime.datetime.strptime(folder_name, 'D%d%m%Y_T%H%M%S')
            except ValueError:
                return None

        dated_folders = [(folder, parse_folder_datetime(folder)) for folder in folders]
        dated_folders = [folder for folder in dated_folders if folder[1] is not None]
        dated_folders.sort(key=lambda x: x[1])
        oldest_folder = dated_folders[0][0]
        oldest_folder_path = os.path.join(results_path, oldest_folder)
        shutil.rmtree(oldest_folder_path)

    def setup_mongo(self, path):
        if self.config["local_mongo_db"]:
            client = MongoClient(self.config["local_mongo_db_port"])
        else:
            client = MongoClient(self.config["remote_mongo_dp_uri"], server_api=ServerApi('1'))
        db = client[self.config["mongo_db_name"]]
        channel_name = path.split("/")[-1].split(".")[0]
        collection = db[channel_name]
        messages = self.message_iter(path)
        return messages, collection
    
    def parse_channel(self, path):
        """
        Parses a channel's messages and stores them in the specified MongoDB database and collection.

        Args:
            path (str): The path to the messages file.
        """
        messages, collection = self.setup_mongo(path)
        for message in messages:
            self.parse_message(message=message, collection=collection)

    def transfer_to_mongoDB(self, folder_name: str, cores: int, max_folders: int):
        """
        Transfers parsed messages to MongoDB, using multiple cores if specified, and manages the result folders.

        Args:
            result_name (str): The name of the result set to transfer.
            cores (int, optional): The number of cores to use for parallel processing. 
            max_folders (int, optional): The maximum number of result folders to keep.
        """
        path_list = self.get_result_path_list(folder_name)
        if cores > 1:
            with ProcessPoolExecutor(max_workers=cores) as executor:
                list(tqdm(executor.map(self.parse_channel, path_list), total=len(path_list), desc=f"Parse {folder_name}", leave=False))
        else:
            for path in tqdm(path_list, total=len(path_list), desc=f"Parse {folder_name}", leave=False):
                self.parse_channel(path=path, cores=cores)
        self.delete_oldest_folder(max_folders=max_folders)
        
    
    def main(self, folder_name:str):
        """
        Scrapes all provided Telegram Channels and saves them as individual collections in a Mongo Database.
        """
        
        self.transfer_to_mongoDB(folder_name=folder_name,
                                cores=self.config["mongo_db_cores"],
                                max_folders=self.config["max_folders"])
