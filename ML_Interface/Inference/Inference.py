from typing import Union, List
from .Classification import Classification
from .Embedding import Embedding

class Inference(Classification, Embedding):
    """
    A class that combines both Classification and Embedding functionalities.
    
    Inherits from:
    - Classification: Handles tasks related to text classification.
    - Embedding: Handles tasks related to generating embeddings.
    
    Methods
    -------
    inference(local: bool, task: str, inputs: Union[str, List[str]]):
        Determines whether to perform an embedding or classification task based on the provided task string.
        Calls the appropriate method based on the task.
    """
    
    def __init__(self) -> None:
        super().__init__()
        
    def inference(self, local: bool, task: str, inputs: Union[str, List[str]]):
        """
        Perform inference based on the task type.
        
        Parameters
        ----------
        local : bool
            Indicates whether to use local processing or API-based processing.
        
        task : str
            The type of task to perform. Should be either an embedding task (e.g., "query-embedding")
            or a classification task (e.g., "factuality-classification").
        
        inputs : Union[str, List[str]]
            The input data to process, which can be a single string or a list of strings.
        
        Returns
        -------
        List
            The result of the embedding or classification task, returned as a list of results.
        """
        if "embedding" in task:
            return self.embedding(local=local, task=task, inputs=inputs)
        else:
            return self.classification(local=local, task=task, inputs=inputs)