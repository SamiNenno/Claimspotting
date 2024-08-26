import os
import json
import pandas as pd
from tqdm import tqdm
from Utils import load_config, get_local_database_path, read_txt_as_list_of_strings, add_key_to_json
from Inference.Inference import Inference


class DataAnnotator(Inference):
    def __init__(self) -> None:
        super().__init__()
        self.load_data()
        self.config = load_config()

    def load_data(self):
        def replace_short_text(text):
            if text is not None and len(text.split()) < 7:
                return None
            return text
        dct_list = list()
        for path in read_txt_as_list_of_strings(os.path.join(get_local_database_path(), "result_path_list.txt")):
            with open(path, "r") as f:
                dct_list.append(json.load(f))
        df = pd.DataFrame(dct_list)
        if len(df) == 0:
            raise ValueError("Download/Annotation/Upload process is aborted because there are no Telegram posts without annotation - System is up to date.")
        df["temp_id"] = df.index
        df["text"] = df["text"].apply(lambda x: replace_short_text(x))
        self.empty_data = df[df["text"].isna()].copy(deep=True).reset_index(drop=True)
        self.data = df[df["text"].notna()].copy(deep=True).reset_index(drop=True)
        
    def add_tag_to_json(self, task:str):
        for idx, row in self.data.iterrows():
            file_path = row["path"]
            new_key = self.config["key_titles"][task]
            new_value = row[task]
            add_key_to_json(file_path=file_path, new_key=new_key, new_value=new_value)
        for idx, row in self.empty_data.iterrows():
            file_path = row["path"]
            new_key = self.config["key_titles"][task]
            new_value = None
            add_key_to_json(file_path=file_path, new_key=new_key, new_value=new_value)
            
    def add_embedding_to_json(self, task:str, outputs:list):
        for idx, row in self.data.iterrows():
            file_path = row["path"]
            new_key = task
            new_value = outputs[idx]
            add_key_to_json(file_path=file_path, new_key=new_key, new_value=new_value) 
        for idx, row in self.empty_data.iterrows():
            file_path = row["path"]
            new_key = task
            new_value = None
            add_key_to_json(file_path=file_path, new_key=new_key, new_value=new_value) 
        
    def tag(self, local: bool, task:str):
        outputs = self.inference(local=local, task=task, inputs=self.data["text"].to_list())
        self.data[task] = outputs
        self.add_tag_to_json(task=task)
        
    def tag_all(self, local:bool):
        ml_tasks = ['topic-classification', #1496MiB VRAM for local application
                      'narrative-classification',  #1496MiB VRAM for local application
                      'factuality-classification', #1496MiB VRAM for local application
                      'polarization-classification', 
                      'sensationalism-classification', 
                      ]
        for task in tqdm(ml_tasks, total=len(ml_tasks), desc="ML Classification", leave=False):
            self.tag(local=local, task=task)
            
    def embed(self, local:bool):
        progress_bar = tqdm(total=2, desc="ML Embedding", unit="step", leave=False)
        task = "document-embedding"
        outputs = self.inference(local=local, task=task, inputs=self.data["text"].to_list())
        self.add_embedding_to_json(task=task, outputs=outputs)
        progress_bar.update(1)
        task = "query-embedding"
        outputs = self.inference(local=local, task=task, inputs=self.data["text"].to_list())
        self.add_embedding_to_json(task=task, outputs=outputs)
        progress_bar.update(1)
    
    def annotate(self, local:bool):
        self.tag_all(local=local)
        self.embed(local=local)

