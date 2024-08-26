import os
from datetime import datetime, timedelta
from typing import List, Optional, Union
from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoStatsInterface():
    def __init__(self) -> None:
        self.client = MongoClient(os.environ['MONGO_DB_URI'], server_api=ServerApi('1'))
        self.db = self.client[os.environ['MONGO_DB_STATS_NAME']]
    
    def remove_id(self, all_documents:list):
        results = list()
        for doc in all_documents:
            doc.pop("_id")
            results.append(doc)
        return results
    
    def fetch_documents_by_date_range(
        self,
        start_day: Union[str, datetime] = None,
        end_day: Optional[Union[str, datetime]] = None,
        channel_names: Optional[List[str]] = None
                ) -> List[dict]:
        """
        Fetch documents from specified collections based on Access_datetime within a date range.

        Parameters:
        - start_day (Union[str, datetime]): The start date as a string in 'YYYY-MM-DD' format or a datetime object
        (default is '2024-07-01').
        - end_day (Optional[Union[str, datetime]]): The end date as a string in 'YYYY-MM-DD' format or a datetime object 
        (default is now).
        - channel_names (Optional[List[str]]): A list of collection names to fetch documents from 
        (default is ['all_collections']).

        Returns:
        - List[dict]: A list of documents that fall within the specified date range.
        """
        if start_day:
            if isinstance(start_day, str):
                start_date = datetime.strptime(start_day, '%Y-%m-%d')
            else:
                start_date = start_day
        else:
            start_date = datetime.strptime("2024-07-01", '%Y-%m-%d')

        if end_day:
            if isinstance(end_day, str):
                end_date = datetime.strptime(end_day, '%Y-%m-%d')
            else:
                end_date = end_day
        else:
            end_date = datetime.now()

        if channel_names is None:
            channel_names = ["all_channels"]

        query = {
                'Access_datetime': {
                    '$gte': start_date,
                    '$lt': end_date + timedelta(days=1)
                }
            }
        all_documents = []

        for channel_name in channel_names:
            collection = self.db[channel_name]
            documents = collection.find(query)
            all_documents.extend(documents)

        all_documents = self.remove_id(all_documents=all_documents)
        self.client.close()

        return all_documents
