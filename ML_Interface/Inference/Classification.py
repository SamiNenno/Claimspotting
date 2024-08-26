import os
import torch
from typing import Union, List
from transformers import pipeline
from .Utils import get_checkpoint, get_endpoint, clear_gpu_memory
os.environ['TOKENIZERS_PARALLELISM'] = "TRUE"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class LocalClassification():
    def __init__(self) -> None:
        pass
    
    def local_load_classifier(self, task:str):
        tokenizer_kwargs = {'padding':True,'truncation':True,'max_length':512}
        checkpoint = get_checkpoint(task)
        classifier = pipeline("text-classification", 
                                model = checkpoint, 
                                tokenizer=checkpoint,
                                torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
                                **tokenizer_kwargs, 
                                device=DEVICE)
        return classifier
    
    def local_classification(self, task:str, inputs: Union[str, List[str]]):
        classifier = self.local_load_classifier(task=task)
        outputs = classifier(inputs)
        del classifier
        clear_gpu_memory()
        return [out["label"] for out in outputs]
    
    
class APIClassification():
    def __init__(self) -> None:
        pass
    
    def api_classification(self, task:str, inputs: Union[str, List[str]]):
        ##https://huggingface.co/blog/inference-endpoints-llm
        pass


class Classification(APIClassification, LocalClassification):
    def __init__(self) -> None:
        super().__init__()
        
    def classification(self, local:bool, task:str, inputs: Union[str, List[str]]):
        if local:
            return self.local_classification(task=task, inputs=inputs)
        else:
            return self.api_classification(task=task, inputs=inputs)