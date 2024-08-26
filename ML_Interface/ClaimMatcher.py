import os
import json
from tqdm import tqdm
from typing import List, Union
from datetime import datetime
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from Utils import load_config, get_local_database_path, read_txt_as_list_of_strings


class ClaimMatcher():
    """
    A class to handle the matching of claims in a MongoDB database using vector search.
    
    Attributes:
    ----------
    config : dict
        Configuration data loaded from an external source.
    numCandidates : int
        Number of candidate matches to retrieve from the vector search.
    limit : int
        Maximum number of results to return from the vector search.
    cosine_cutoff : float
        Cosine similarity cutoff value, projected for MongoDB vector search.
    index : str
        The name of the Atlas Search index used for vector search.
    sort_by_date : bool
        Whether to sort the results by their publishing date.
    client : pymongo.MongoClient
        MongoDB client for interacting with the database.
    db : pymongo.database.Database
        The specific database within MongoDB to perform vector search.
    collection : pymongo.collection.Collection
        The collection within the MongoDB database where vector data is stored.
    dct_list : list
        A list of dictionaries loaded from JSON files containing claim data.
    """
    
    def __init__(self) -> None:
        """
        Initializes the ClaimMatcher with configuration data, loads the claim data, 
        and connects to MongoDB.
        """
        self.load_data()
        self.config = load_config()
        self.numCandidates = self.config["claim_matching_paramters"]["numCandidates"]
        self.limit = self.config["claim_matching_paramters"]["limit"]
        self.cosine_cutoff = self.project_cos_to_mongo(self.config["claim_matching_paramters"]["cosine_cutoff"])
        self.index = self.config["claim_matching_paramters"]["atlas_index_name"]
        self.sort_by_date = self.config["claim_matching_paramters"]["sort_by_date"]
        self.client = MongoClient(self.config["mongo_db"]["remote_mongo_dp_uri"], server_api=ServerApi('1'))
        self.db = self.client[self.config["mongo_db"]["mongo_vector_db_name"]]
        self.collection = self.db[self.config["mongo_db"]["mongo_vector_db_name"]]

    def load_data(self) -> None:
        """
        Loads claim data from JSON files specified in a text file and stores them in a list.
        Raises a ValueError if no data is loaded.
        """
        self.dct_list = list()
        for path in read_txt_as_list_of_strings(os.path.join(get_local_database_path(), "result_path_list.txt")):
            with open(path, "r") as f:
                self.dct_list.append(json.load(f))
        if len(self.dct_list) == 0:
            raise ValueError("Download/Annotation/Upload process is aborted because there are no Telegram posts without annotation - System is up to date.")
        
    def project_cos_to_mongo(self, cosine_cutoff: float = 0.91) -> float:
        """
        Projects a cosine similarity cutoff value to MongoDB's vector search score range.
        
        Parameters:
        ----------
        cosine_cutoff : float, optional
            The cosine similarity cutoff value (default is 0.91).
        
        Returns:
        -------
        float
            The projected MongoDB vector search score.
        """
        # https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/
        return (1 + cosine_cutoff) / 2

    def remove_by_cos(self, query_results: list) -> list:
        """
        Filters query results by removing those below the cosine similarity cutoff.
        
        Parameters:
        ----------
        query_results : list
            A list of query results from the vector search.
        
        Returns:
        -------
        list
            A filtered list of query results that meet the cosine similarity cutoff.
        """
        return [r for r in query_results if r["score"] >= self.cosine_cutoff]
    
    def sort_results_by_date(self, query_results: list) -> list:
        """
        Sorts the query results by their publishing date in descending order.
        
        Parameters:
        ----------
        query_results : list
            A list of query results from the vector search.
        
        Returns:
        -------
        list
            A list of query results sorted by their publishing date.
        """
        query_results = sorted(query_results, key=lambda x: datetime.strptime(x['Publishing_datetime'], "%Y-%m-%d %H:%M:%S"), reverse=True)
        return query_results
    
    def vector_search(self, query_embedding: List[float]) -> list:
        """
        Performs a vector search in the MongoDB collection using the provided query embedding.
        
        Parameters:
        ----------
        query_embedding : List[float]
            The embedding vector used for the search query.
        
        Returns:
        -------
        list
            A list of query results containing matches for the provided embedding.
        """
        query_results = self.collection.aggregate([
        {"$vectorSearch": {
            "queryVector": query_embedding,
            "path": "text_embedding",
            "numCandidates": self.numCandidates,
            "limit": self.limit,
            "index": self.index,
            },
        },
        {
            "$project": {
            "post_id":1,
            "Link": 1,
            "Channel_Name": 1,
            "Publishing_datetime": 1,
            "score": { "$meta": "vectorSearchScore" }
            }
        }
        ])
        return query_results
    
    def query(self, 
              query_embedding: List[float], 
              _id: Union[str, None] = None
              ) -> list:
        """
        Queries the MongoDB collection using a query embedding, optionally filtering out results by ID, 
        and sorting by date if specified.
        
        Parameters:
        ----------
        query_embedding : List[float]
            The embedding vector used for the search query.
        _id : Union[str, None], optional
            The ID to exclude from the query results (default is None).
        
        Returns:
        -------
        list
            A list of query results after filtering and sorting.
        """
        query_results = self.vector_search(query_embedding=query_embedding)
        if not query_results:
            return []
        query_results = self.remove_by_cos(query_results=query_results)
        for r in query_results:
            r["_id"] = str(r["_id"])
        if _id is not None:
            query_results = [r for r in query_results if not r["_id"] == _id]
        if self.sort_by_date:
            query_results = self.sort_results_by_date(query_results=query_results)
        return query_results
    
    def match_claims(self) -> None:
        """
        Matches claims based on their embeddings and updates the corresponding JSON files with the results.
        """
        for dct in tqdm(self.dct_list, total=len(self.dct_list), desc="Claim matching", leave=False):
            query_embedding = dct["query-embedding"]
            _id = dct["_id"]
            if query_embedding is None:
                dct["Siblings"] = []
            else:
                dct["Siblings"] = self.query(query_embedding=query_embedding, _id=_id)
            with open(dct["path"], 'w') as json_file:
                json.dump(dct, json_file, indent=4)
                
if __name__ == "__main__":
    ClaimMatcher().match_claims()
