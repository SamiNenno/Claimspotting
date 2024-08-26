import argparse
from time import sleep
from typing import Union
from MongoDownloader import MongoDownloader
from Annotator import DataAnnotator
from MongoUploader import MongoUploader
from ClaimMatcher import ClaimMatcher
from MatchUploader import MatchUploader

class Interface():
    def __init__(self) -> None:
        pass
    
    def main(self, local: Union[bool, int], key_title: str = "Topic"):
        if isinstance(local, int):
            local = bool(local)
        
        MongoDownloader().download(key_title=key_title)
        DataAnnotator().annotate(local=local)
        MongoUploader().upload()
        sleep(60 * 2) # Give MongoDB 2 minutes to index the new documents.
        ClaimMatcher.match_claims()
        MatchUploader.upload()

def parse_arguments():
    """
    Parses command-line arguments using argparse.

    Returns:
    argparse.Namespace: The parsed arguments as attributes.
    """
    parser = argparse.ArgumentParser(description="Run the Interface for downloading, annotating, and uploading data.")
    
    # Add arguments
    parser.add_argument(
        '--local', 
        type=int, 
        help='1 if machine learning models should be locally deployed and 0 if a cloud service should be used (currently huggingface inference endpoints).'
    )
    parser.add_argument(
        '--key_title', 
        type=str, 
        default='Topic', 
        help='The key to use for downloading documents. All documents without that key will be downloaded. Default is "Topic".'
    )
    
    # Parse arguments
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    Interface().main(local=args.local, key_title=args.key_title)
