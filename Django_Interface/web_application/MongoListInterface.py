import os
from pathlib import Path
from tqdm import tqdm
from typing import Union, List
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi


PROJECT_DIRECTORY = str(Path(__file__).resolve().parent)

class MongoListInterface:
    """
    A class to interact with MongoDB and perform various operations such as concatenating strings, 
    fetching nested values, converting labels to binary, and retrieving documents within a specified date range.
    """

    def __init__(self) -> None:
        """
        Initializes the MongoListInterface object. Connects to the MongoDB database using the URI and database 
        name provided in the environment variables. Sets up dictionaries for label conversion and topic translation.
        """
        self.client = MongoClient(os.environ['MONGO_DB_URI'], server_api=ServerApi('1'))
        self.db = self.client[os.environ['MONGO_DB_NAME']]
        self.label2id = {
            "factual": 1,
            "polarization": 1,
            "sensational": 1,
            "non-factual": 0,
            "non-polarization": 0,
            "non-sensational": 0,
        }
        self.topic_en2de =  {
            "Agriculture": "Landwirtschaft",
            "Civil Rights": "Bürgerrechte",
            "Culture": "Kultur",
            "Defense": "Verteidigung",
            "Domestic Commerce": "Binnenhandel",
            "Education": "Bildung",
            "Energy": "Energie",
            "Environment": "Umwelt",
            "European Union": "Europäische Union",
            "Foreign Trade": "Außenhandel",
            "Government Operations": "Staatsbetrieb",
            "Health": "Gesundheit",
            "Housing": "Wohnungswesen",
            "Immigration": "Migration und Integration",
            "International Affairs": "Internationale Angelegenheiten",
            "Labor": "Arbeit und Beschäftigung",
            "Law and Crime": "Recht und Kriminalität",
            "Macroeconomics": "Makroökonomie",
            "Non-thematic": "Kein Thema",
            "Other": "Sonstiges",
            "Social Welfare": "Sozialstaat",
            "Technology": "Technologie, Wissenschaft und Kommunikation",
            "Transportation": "Transport"
        }
        
    def remove_russian_channels(self, collection_names:List[str]):
        """
        This function takes in collection_names and removes collections with posts in Russian.

        :param collection_names: List of strings to be filtered
        :return: Filtered list with Russian channels removed
        """
        with open(os.path.join(PROJECT_DIRECTORY,"russian_channels.txt"), 'r') as file:
            russian_channels = [line.strip() for line in file.readlines()]
        temp = list()
        for collection_name in collection_names:
            if collection_name.strip() not in russian_channels:
                temp.append(collection_name)
        collection_names = temp
        return collection_names

    def concatenate_strings(self, text: Union[str, None], caption: Union[str, None]) -> Union[str, None]:
        """
        Concatenates two strings, ignoring any None values.

        Parameters:
        text (str or None): The first string or None.
        caption (str or None): The second string or None.

        Returns:
        str or None: The concatenated result of the non-None strings, or None if both are None.
        """
        concat = ' '.join(filter(None, [text, caption]))
        concat = None if concat == '' else concat
        return concat
    
    def get_nested_values(self, doc: dict, key1: str, key2: str) -> Union[str, None]:
        """
        Retrieves a nested value from a document.

        Parameters:
        doc (dict): The document from which to retrieve the value.
        key1 (str): The first key to access the nested dictionary.
        key2 (str): The second key to access the desired value in the nested dictionary.

        Returns:
        str or None: The value associated with the nested key, or None if it does not exist.
        """
        res = doc.get(key1)
        if res is None:
            return None
        else:
            return res[-1].get(key2)
        
    def get_binary(self, label: Union[str, None]) -> int:
        """
        Converts a label into a binary value based on the predefined label2id mapping.

        Parameters:
        label (str or None): The label to convert.

        Returns:
        int: The binary value corresponding to the label. Defaults to 0 if the label is not found.
        """
        return self.label2id.get(label, 0)
    
    def check_if_many_siblings(self, doc: dict, cutoff: int) -> int:
        """
        Checks if a document has many sibling links.

        Parameters:
        doc (dict): The document to check for siblings.
        cutoff (int): The threshold number of siblings to determine if the document has many siblings.

        Returns:
        int: 1 if the number of siblings is greater than or equal to the cutoff, otherwise 0.
        """
        siblings = doc.get("Siblings")
        if siblings is None:
            return 0
        elif isinstance(siblings, list):
            if len(siblings) >= cutoff:
                return 1
            else:
                return 0
        else:
            return 0
        
    def standardize_engagement(self, parsed_doc: dict) -> dict:
        """
        Standardizes the engagement metrics (views and forwards) by the member count.

        Parameters:
        parsed_doc (dict): The parsed document containing engagement metrics and member count.

        Returns:
        dict: The document with standardized engagement metrics.
        """
        if isinstance(parsed_doc["Member_count"], (float, int)):
            if isinstance(parsed_doc["Views"], (float, int)):
                parsed_doc["Views_standard"] = parsed_doc["Views"] / parsed_doc["Member_count"]
            else:
                parsed_doc["Views_standard"] = None
            if isinstance(parsed_doc["Forwards"], (float, int)):
                parsed_doc["Forwards_standard"] = parsed_doc["Forwards"] / parsed_doc["Member_count"]
            else:
                parsed_doc["Forwards_standard"] = None
        else:
            parsed_doc["Views_standard"] = None
            parsed_doc["Forwards_standard"] = None
        return parsed_doc
    
    def sort_results_by_date(self, documents: list) -> list:
        """
        Sorts documents by their publishing date in descending order.

        Parameters:
        documents (list): A list of documents to sort.

        Returns:
        list: A list of documents sorted by their publishing date.
        """
        documents = sorted(documents, key=lambda x: x['Publishing_datetime'], reverse=True)
        return documents
    
    def parse_document(self, doc: dict, cutoff: int) -> dict:
        """
        Parses a document from the database and extracts relevant fields, performing transformations as necessary.

        Parameters:
        doc (dict): The document to be parsed. This is typically a dictionary representing a record from a MongoDB collection.
        cutoff (int): The threshold used to determine if the document has "many siblings." This is used in the 
        `check_if_many_siblings` method to categorize the document based on the number of sibling links.

        Returns:
        dict: A dictionary containing the parsed and transformed document.
        """
        parsed_doc = {
            "Message_ID": doc.get("Message_ID"),
            "Channel_Name": doc.get("Channel_Name"),
            "Link": doc.get("Link"),
            "Publishing_datetime": doc.get("Publishing_datetime"),
            "Member_count": self.get_nested_values(doc=doc, key1="Member_count", key2="Member_count"),
            "Views": self.get_nested_values(doc=doc, key1="Engagement", key2="Views"),
            "Forwards": self.get_nested_values(doc=doc, key1="Engagement", key2="Forwards"),
            "Text": self.concatenate_strings(
                text=self.get_nested_values(doc=doc, key1="Content", key2="Text"),
                caption=self.get_nested_values(doc=doc, key1="Content", key2="Caption")
            ),
            "Topic": self.topic_en2de.get(doc.get("Topic")),
            "Narratives": doc.get("Narratives"),
            "Factual": self.get_binary(doc.get("Factual")),
            "Polarising": self.get_binary(doc.get("Polarising")),
            "Sensationalist": self.get_binary(doc.get("Sensationalist")),
            "Many_Siblings": self.check_if_many_siblings(doc=doc, cutoff=cutoff),
            "High_Diffusion": None,  # To be implemented
            "Siblings": doc.get("Siblings", [])
        }
        if len(parsed_doc["Siblings"]) > 0:
            parsed_doc["Siblings"] = list(set([s["Link"] for s in parsed_doc["Siblings"]]))
        parsed_doc = self.standardize_engagement(parsed_doc=parsed_doc)
        return parsed_doc
       
    def get_daterange_docs_from_single_collection(
        self, 
        collection_name: str, 
        start_date: Union[datetime, str], 
        end_date: Union[datetime, str], 
        factual: bool,
    ) -> list:
        """
        Retrieves documents from a single collection within a specified date range.

        Parameters:
        collection_name (str): The name of the collection to query.
        start_date (Union[datetime, str]): The start date of the range as a datetime object or string.
        end_date (Union[datetime, str]): The end date of the range as a datetime object or string.
        factual (bool): Whether to return only factual documents.

        Returns:
        list: A list of documents that match the query.
        """
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # Adjust end_date to include the entire day
        end_date = end_date.replace(hour=23, minute=59, second=59)

        query = {
            "Publishing_datetime": {
                "$gte": start_date,  
                "$lte": end_date 
            }
        }
        # Return only factual posts
        if factual:
            query["Factual"] = "factual"
        return self.db[collection_name].find(query)
    
    def get_daterange_docs(
        self, 
        start_date: Union[datetime, str], 
        end_date: Union[datetime, str], 
        collection_names: Union[str, List[str]] = [],
        factual: bool = False,
        cutoff: int = 5,
        remove_russian:bool = True
    ) -> list:
        """
        Retrieves documents from multiple collections within a specified date range.

        Parameters:
        start_date (Union[datetime, str]): The start date of the range as a datetime object or string.
        end_date (Union[datetime, str]): The end date of the range as a datetime object or string.
        collection_names (Union[str, List[str]]): The names of the collections to query. Defaults to all collections if not provided.
        factual (bool): Whether to return only factual documents. Defaults to False.
        cutoff (int): The threshold used to determine if a document has "many siblings."
        remove_russian (bool): Whether to remove russian language only channels. Defaults to True.
        
        Returns:
        list: A list of parsed documents that match the query, sorted by their publishing date.
        """
        documents = list()
        if isinstance(collection_names, str):
            collection_names = [collection_names]
        if not collection_names:
            collection_names = self.db.list_collection_names()
            if remove_russian:
                collection_names = self.remove_russian_channels(collection_names=collection_names)
        for collection_name in tqdm(collection_names, total=len(collection_names), desc="Query MongoDB", leave=False):
            for doc in self.get_daterange_docs_from_single_collection(collection_name=collection_name, start_date=start_date, end_date=end_date, factual=factual):
                documents.append(self.parse_document(doc=doc, cutoff=cutoff))
        documents = self.sort_results_by_date(documents=documents)
        return documents
    
if __name__ == "__main__":
    docs = MongoListInterface().get_daterange_docs("2024-07-30", "2024-07-31", ["neuesausrussland"], True)
    for doc in docs:
        print(doc)
