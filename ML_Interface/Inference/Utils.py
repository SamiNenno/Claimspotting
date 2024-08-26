import gc
import json
import torch
from pathlib import Path

def clear_gpu_memory():
    """
    Clears the GPU memory by emptying the CUDA cache, collecting inter-process communication (IPC) 
    resources, synchronizing the GPU, and running garbage collection.
    
    This function is useful for freeing up GPU resources that are no longer in use, 
    which can help prevent memory leaks and optimize resource utilization.
    """
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()
    torch.cuda.synchronize()
    gc.collect()
    
def make_path(extension: str) -> str:
    """
    Constructs an absolute path by appending the given extension to the project's root directory.

    Parameters:
    extension (str): The relative path or filename to be appended.

    Returns:
    str: The full absolute path as a string.
    """
    project_path = Path(Path(__file__).resolve().parent.parent)
    return str(project_path / extension)

def load_config() -> dict:
    """
    Loads the configuration settings from a JSON file located in the project's root directory.

    Returns:
    dict: The configuration settings as a dictionary.
    """
    with open(make_path(extension="config.json"), "r") as f:
        dct = json.load(f)
    return dct

def get_checkpoint(task: str) -> str:
    """
    Retrieves the checkpoint path for a specific task from the configuration file.

    Parameters:
    task (str): The name of the task for which the checkpoint is required.

    Returns:
    str: The path to the checkpoint file for the specified task.
    """
    return load_config()["checkpoints"].get(task)

def get_endpoint(task: str) -> str:
    """
    Retrieves the API endpoint for a specific task from the configuration file.

    Parameters:
    task (str): The name of the task for which the endpoint is required.

    Returns:
    str: The URL of the API endpoint for the specified task.
    """
    return load_config()["endpoints"].get(task)
