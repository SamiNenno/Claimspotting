import os
import re
import json
from tqdm import tqdm
from typing import Union
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Utils import load_config, get_local_database_path, clear_database, get_timestamp, make_folder, save_list_as_txt

class TextCleaner():
    """
    A class to perform various text cleaning operations such as removing emojis, URLs, hashtags, and more.
    Provides methods to concatenate strings and clean text using a series of cleaning functions.
    """

    def __init__(self) -> None:
        """Initializes the TextCleaner class with no specific attributes."""
        pass
    
    def concatenate_strings(self, text: Union[str, None], caption: Union[str, None]):
        """
        Concatenates two strings, ignoring any None values.

        Parameters:
        text (str or None): The first string or None.
        caption (str or None): The second string or None.

        Returns:
        str: The concatenated result of the non-None strings, or None if both are None.
        """
        concat = ' '.join(filter(None, [text, caption]))
        concat = None if concat == '' else concat
        return concat
    
    def remove_emojis(self, input_string:str):
        """
        Removes emojis from the input string.

        Parameters:
        input_string (str): The string from which emojis will be removed.

        Returns:
        str: The input string without emojis.
        """
        emoji_pattern = re.compile(
            "["                     
            "\U0001F600-\U0001F64F" 
            "\U0001F300-\U0001F5FF" 
            "\U0001F680-\U0001F6FF" 
            "\U0001F1E0-\U0001F1FF" 
            "\U00002702-\U000027B0" 
            "\U000024C2-\U0001F251" 
            "\U0001F900-\U0001F9FF" 
            "\U0001F018-\U0001F270" 
            "\U0001F780-\U0001F7F0" 
            "\U0001F000-\U0001F02F" 
            "]+", flags=re.UNICODE
        )
        return emoji_pattern.sub(r'', input_string).strip()
    
    def replace_urls(self, input_string:str):
        """
        Replaces URLs in the input string with a placeholder "<URL>".

        Parameters:
        input_string (str): The string from which URLs will be replaced.

        Returns:
        str: The input string with URLs replaced by "<URL>".
        """
        url_pattern = re.compile(r'http[s]?://\S+|www\.\S+')
        text_without_urls = url_pattern.sub("<URL>", input_string)
        return text_without_urls.strip()

    def remove_hashtags(self, input_string:str):
        """
        Removes hashtags from the input string.

        Parameters:
        input_string (str): The string from which hashtags will be removed.

        Returns:
        str: The input string without hashtags.
        """
        hashtag_pattern = re.compile(r'#\w+')
        return hashtag_pattern.sub('', input_string).strip()

    def remove_at(self, input_string:str):
        """
        Removes mentions (starting with @) from the input string.

        Parameters:
        input_string (str): The string from which mentions will be removed.

        Returns:
        str: The input string without mentions.
        """
        hashtag_pattern = re.compile(r'@\w+')
        return hashtag_pattern.sub('', input_string).strip()

    def remove_multiple_spaces(self, input_string:str):
        """
        Replaces multiple spaces in the input string with a single space.

        Parameters:
        input_string (str): The string in which multiple spaces will be replaced.

        Returns:
        str: The input string with multiple spaces replaced by a single space.
        """
        return re.sub(r'\s+', ' ', input_string).strip()

    def remove_multiple_tabs(self, input_string:str):
        """
        Replaces multiple tabs in the input string with a single space.

        Parameters:
        input_string (str): The string in which multiple tabs will be replaced.

        Returns:
        str: The input string with multiple tabs replaced by a single space.
        """
        return re.sub(r'\t+', ' ', input_string).strip()
    
    def remove_newlines(self, input_string:str):
        """
        Removes newlines from the input string.

        Parameters:
        input_string (str): The string from which newlines will be removed.

        Returns:
        str: The input string without newlines.
        """
        return input_string.replace("\n", " ")

    def clean(self, text: Union[str, None], caption: Union[str, None]):
        """
        Cleans the input strings by concatenating them and applying various text cleaning methods.

        Parameters:
        text (str or None): The first string to be cleaned.
        caption (str or None): The second string to be cleaned.

        Returns:
        str or None: The cleaned text or None if both inputs are None.
        """
        text = self.concatenate_strings(text=text, caption=caption)
        if text is None:
            return text
        text = self.remove_emojis(input_string=text)
        text = self.replace_urls(input_string=text)
        text = self.remove_hashtags(input_string=text)
        text = self.remove_at(input_string=text)
        text = self.remove_multiple_spaces(input_string=text)
        text = self.remove_multiple_tabs(input_string=text)
        text = self.remove_newlines(input_string=text)
        return text
    
class MongoDownloader(TextCleaner):
    """
    A class to interact with a MongoDB database, download documents, clean text, and save the results as JSON files.
    Inherits from the TextCleaner class to use its text cleaning methods.
    """

    def __init__(self) -> None:
        """Initializes the MongoDownloader class with MongoDB client and configuration settings."""
        super().__init__()
        self.config = load_config()
        self.client = MongoClient(self.config["mongo_db"]["remote_mongo_dp_uri"], server_api=ServerApi('1'))
        self.db = self.client[self.config["mongo_db"]["mongo_db_name"]]
        self.collection_names = self.db.list_collection_names()
        self.json_path_list = list()
        
    def save_result_path(self):
        """
        Saves the list of JSON file paths to a text file.
        """
        result_path = os.path.join(get_local_database_path(), "result_path_list.txt")
        save_list_as_txt(file_path=result_path, data=self.json_path_list)
        
    def create_database_folder(self):
        """
        Creates a folder to store the downloaded documents, named with the current timestamp.

        Returns:
        str: The path to the created database folder.
        """
        database_folder = os.path.join(get_local_database_path(), get_timestamp())
        make_folder(database_folder)
        return database_folder
    
    def get_collection(self, collection_name:str):
        """
        Retrieves a MongoDB collection by name.

        Parameters:
        collection_name (str): The name of the collection to retrieve.

        Returns:
        Collection: The MongoDB collection object.
        """
        return self.db[collection_name]
    
    def get_docs_without_key(self, collection_name:str, key_title:str):
        """
        Retrieves documents from a MongoDB collection that do not have a specific key.

        Parameters:
        collection_name (str): The name of the collection to query.
        key_title (str): The key to check for existence.

        Returns:
        Cursor: A cursor to the documents that do not have the specified key.
        """
        query = {key_title: {"$exists": False}}
        return self.get_collection(collection_name=collection_name).find(query)
    
    def parse_doc(self, doc:dict, json_path:str):
        """
        Parses a document and cleans its text content.

        Parameters:
        doc (dict): The document to parse.
        json_path (str): The path where the parsed document will be saved.

        Returns:
        dict: The parsed and cleaned document.
        """
        return {
            "_id":str(doc["_id"]),
            "channel": doc["Channel_Name"],
            "datetime":doc["Publishing_datetime"].strftime('%Y-%m-%d %H:%M:%S'),
            "link":doc["Link"],
            "path":json_path,
            "text": self.clean(text=doc["Content"][-1]["Text"], caption=doc["Content"][-1]["Caption"])
        }
    
    def save_collection(self, database_folder:str, collection_name:str, key_title:str):
        """
        Saves documents from a MongoDB collection as JSON files in a specified folder.

        Parameters:
        database_folder (str): The folder where the JSON files will be saved.
        collection_name (str): The name of the collection to download.
        key_title (str): The key to filter documents by (documents without this key will be downloaded).
        """
        collection_folder = os.path.join(database_folder, collection_name)
        make_folder(collection_folder)
        for idx, doc in enumerate(self.get_docs_without_key(collection_name=collection_name, key_title=key_title)):
            json_path = os.path.join(collection_folder, f"{idx}.json")
            doc = self.parse_doc(doc=doc, json_path=json_path)
            with open(json_path, 'w', encoding='utf-8') as json_file:
                json.dump(doc, json_file, ensure_ascii=False, indent=4)
            self.json_path_list.append(json_path)

    def download(self, key_title:str = "Topic"):
        """
        Downloads documents from all MongoDB collections, cleans their text, and saves them as JSON files.

        Parameters:
        key_title (str): The key to filter documents by (default is "Topic").
        """
        database_folder = self.create_database_folder()
        for idx, collection_name in tqdm(enumerate(self.collection_names), total=len(self.collection_names), desc="Download unlabeled documents", leave=False):
            self.save_collection(database_folder=database_folder, collection_name=collection_name, key_title=key_title)
        clear_database()
        self.save_result_path()
        self.client.close()
