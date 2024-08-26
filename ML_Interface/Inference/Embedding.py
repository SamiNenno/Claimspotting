import torch
from typing import Union, List
from huggingface_hub import InferenceClient
from sentence_transformers import SentenceTransformer
from .Utils import get_checkpoint, get_endpoint, load_config, clear_gpu_memory


BATCH_SIZE = 128
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class LocalEmbedding():
    """
    A class to handle embeddings using a local pre-trained SentenceTransformer model.
    
    Methods
    -------
    embed_query(inputs: Union[str, List[str]], model):
        Embeds a query string or a list of query strings using the provided model.
        
    embed_documents(inputs: Union[str, List[str]], model):
        Embeds a document or a list of documents using the provided model.
        
    local_embedding(task: str, inputs: Union[str, List[str]]):
        Handles the embedding process locally based on the task (query or document embedding).
    """
    
    def __init__(self) -> None:
        pass
    
    def embed_query(self, inputs: Union[str, List[str]], model):
        return model.encode(sentences=inputs, 
                    prompt="Instruct: Retrieve semantically similar text.\nQuery: ",
                    batch_size=BATCH_SIZE,
                    show_progress_bar=False,
                    normalize_embeddings=False,
                    convert_to_numpy=True,
                    device=DEVICE)
        
    def embed_documents(self, inputs: Union[str, List[str]], model):
        return model.encode(sentences=inputs, 
                    batch_size=BATCH_SIZE,
                    show_progress_bar=False,
                    normalize_embeddings=False,
                    convert_to_numpy=True,
                    device=DEVICE)

    def local_embedding(self, task:str, inputs: Union[str, List[str]]):
        model = SentenceTransformer(get_checkpoint(task))
        embed = self.embed_query if task == "query-embedding" else self.embed_documents
        embeddings = embed(inputs=inputs, model=model)
        del model
        clear_gpu_memory()
        return [e.tolist() for e in embeddings]
    
class APIEmbedding():
    """
    A class to handle embeddings through an external API, specifically the Hugging Face Inference API.
    
    Methods
    -------
    add_prompt(inputs: Union[str, List[str]]):
        Adds a specific prompt to the inputs if the task is query embedding.
        
    api_embedding(task: str, inputs: Union[str, List[str]]):
        Handles the embedding process via the API based on the task (query or document embedding).
    """
    
    def __init__(self) -> None:
        pass
    
    def add_prompt(self, inputs: Union[str, List[str]]):
        return [f"Instruct: Retrieve semantically similar text.\nQuery: {i}" for i in inputs]
    
    def api_embedding(self, task:str, inputs: Union[str, List[str]]):
        if task == "query-embedding":
            inputs = self.add_prompt(inputs=inputs)
        endpoint = get_endpoint(task=task)
        hf_token = load_config()["hf_token"]
        client = InferenceClient(endpoint, token=hf_token)
        embeddings = client.feature_extraction(text=inputs, normalize=False, truncate=True)
        return embeddings.tolist()

    
class Embedding(APIEmbedding, LocalEmbedding):
    """
    A class that combines both local and API-based embedding capabilities.
    
    Methods
    -------
    embedding(local: bool, task: str, inputs: Union[str, List[str]]):
        Selects between local embedding and API embedding based on the `local` flag.
    """
    
    def __init__(self) -> None:
        super().__init__()
    
    def embedding(self, local:bool, task:str, inputs: Union[str, List[str]]):
        if local:
            return self.local_embedding(task=task, inputs=inputs)
        else:
            return self.api_embedding(task=task, inputs=inputs)

if __name__ == "__main__":
    print(get_checkpoint("query-embedding"))