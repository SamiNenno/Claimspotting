import os
import requests
from typing import List
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class MongoSearchInterface():
    """
    A class to perform vector-based search queries against a MongoDB collection using sentence embeddings.
    It uses a pre-trained sentence transformer model to embed query texts and retrieve semantically similar
    documents from the database. The search results can be filtered by a cosine similarity threshold and
    duplicates can be removed.

    Attributes:
    -----------
    client : pymongo.MongoClient
        The MongoDB client for connecting to the MongoDB database.
    collection : pymongo.collection.Collection
        The specific MongoDB collection where the vector data is stored.
    cosine_cutoff : float
        The cosine similarity threshold used to filter out less relevant results.
    """

    def __init__(self, cosine_cutoff: float = .91) -> None:
        """
        Initializes the `FakeSearch` object with MongoDB connection parameters, model checkpoint,
        and a cosine similarity cutoff.

        Parameters:
        -----------
        cosine_cutoff : float, optional
            The cutoff for cosine similarity. Defaults to 0.91. The actual threshold used in the search
            is `(1 + cosine_cutoff) / 2`.
        """
        self.client = MongoClient(os.environ['MONGO_DB_URI'], server_api=ServerApi('1'))
        self.collection = self.client[os.environ['MONGO_VECTOR_DB_NAME']][os.environ['MONGO_VECTOR_DB_NAME']]
        self.cosine_cutoff = (1 + cosine_cutoff) / 2

    def embed_query(self, query_text:str):
        headers = {
        "Authorization": f"Bearer {os.environ['RUNPOD_API_KEY']}",
        "Content-Type": "application/json"
        }
        url = f"https://api.runpod.ai/v2/{os.environ['RUNPOD_ENDPOINT']}/runsync"
        data = {
            "input": {
                "input": query_text,
                "model":"Sami92/multiling-e5-large-instruct-claim-matching"
            }
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()["output"]["data"][0]["embedding"]

    def embed_query_openai(self, query_text: str):
        """
        Generates an embedding for the given query text using the OpenAI API via RunPod.

        This function interacts with the OpenAI API hosted on RunPod to generate a semantic embedding 
        of the provided query text. The embedding is created using the model 
        "Sami92/multiling-e5-large-instruct-claim-matching". The function constructs a prompt and 
        sends it to the API, then returns the resulting embedding vector.

        Parameters:
        -----------
        query_text : str
            The input text for which the semantic embedding is to be generated.

        Returns:
        --------
        List[float]
            The embedding vector generated for the input text.

        """
        #from openai import OpenAI
        #https://github.com/runpod-workers/worker-infinity-embedding
        #client = OpenAI(
        #    api_key=os.environ['RUNPOD_API_KEY'],
        #    base_url=f"https://api.runpod.ai/v2/{os.environ['RUNPOD_ENDPOINT']}/openai/v1"
        #)
        #embedding = client.embeddings.create(
        #    model="Sami92/multiling-e5-large-instruct-claim-matching",
        #    input=f"Instruct: Retrieve semantically similar text.\nQuery: {query_text}",
        #)
        #return embedding.data[0].embedding
        pass

    def remove_duplicates(self, query_results: list) -> list:
        """
        Removes duplicate results from the query results based on the `Link` key.

        Parameters:
        -----------
        query_results : list
            A list of dictionaries representing the query results.

        Returns:
        --------
        list
            A list of dictionaries with duplicate entries removed.
        """
        seen_links = set()
        unique_dicts = []

        for d in query_results:
            link = d.get("Link")
            if link not in seen_links:
                seen_links.add(link)
                d.pop("_id")
                d.pop("score")
                unique_dicts.append(d)
        return unique_dicts

    def remove_by_cos(self, query_results: list) -> list:
        """
        Filters the query results by removing entries below the cosine similarity cutoff.

        Parameters:
        -----------
        query_results : list
            A list of dictionaries representing the query results.

        Returns:
        --------
        list
            A list of dictionaries filtered by the cosine similarity cutoff.
        """
        return [r for r in query_results if r["score"] >= self.cosine_cutoff]

    def query_database(self, embedding: List[float]) -> list:
        """
        Queries the MongoDB collection using the provided embedding vector and retrieves
        matching documents based on vector similarity.

        Parameters:
        -----------
        embedding : List[float]
            The embedding vector to use for the query.

        Returns:
        --------
        list
            A list of dictionaries representing the matching documents, filtered by cosine similarity
            and with duplicates removed.
        """
        query_results = self.collection.aggregate([
            {"$vectorSearch": {
                "queryVector": embedding,
                "path": "text_embedding",
                "numCandidates": 200,
                "limit": 50,
                "index": "claim_matching_index",
                },
            },
            {
                "$project": {
                "Link": 1,
                "Channel_Name": 1,
                "Publishing_datetime": 1,
                "score": { "$meta": "vectorSearchScore" }
                }
            }
            ])
        query_results = self.remove_by_cos(query_results=query_results)
        query_results = self.remove_duplicates(query_results=query_results)
        return query_results

    def search(self, query_text: str) -> list:
        """
        Performs a search for semantically similar documents based on the input query text.

        Parameters:
        -----------
        query_text : str
            The input query text to search for.

        Returns:
        --------
        list
            A list of dictionaries representing the matching documents.
        """

        embedding = self.embed_query(query_text=query_text)
        result = self.query_database(embedding=embedding)
        return result


if __name__ == "__main__":
    query_text="Das rumänische Verteidigungsministerium hat einen Bericht über die Ergebnisse der Ausbildung ukrainischer Piloten auf F-16-Jägern erstellt. von 50 Kadetten sind nur drei bereit, die F-16 zu fliegen" 
    res = MongoSearchInterface().search(query_text=query_text)
    print(res)