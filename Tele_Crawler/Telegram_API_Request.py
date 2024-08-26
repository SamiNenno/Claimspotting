import os
import json
import time
import logging
import asyncio
import datetime
import numpy as np
from tqdm import tqdm
from glob import glob
from pathlib import Path
from pyrogram import Client
from pyrogram.errors import RPCError
from pyrogram.errors.exceptions.flood_420 import FloodWait
from MessageParser import MessageParser
logging.getLogger('pyrogram').setLevel(logging.WARNING)



class Telegram_Scraper(MessageParser):
    """
    Telegram_Scraper provides methods to access the Telegram API and retrieve messages from specified channels.

    This class uses configurations from './Utils/config.json' to access channels listed in './Utils/Telegram_Channels'.
    It writes the retrieved messages to JSON files.

    Attributes:
        session_counter (int): Counter to keep track of the number of API sessions.
        config (dict): Configuration parameters loaded from './Utils/config.json'.
        credential_keys (list): List of credential keys for accessing the Telegram API.
        credentials (dict): Current API credentials used for accessing the Telegram API.
        progress_bar (tqdm.tqdm): Progress bar for tracking message retrieval.

    Methods:
        __init__():
            Initializes the Telegram_Scraper instance.
        load_credential_keys():
            Loads credential keys from the configuration file.
        load_credentials():
            Loads the Telegram API credentials for the current session.
        channel_iter():
            Iterates over channel configuration files and yields their content.
        access_api(channel_name: str) -> list:
            Asynchronously accesses the Telegram API to retrieve messages from a specified channel.
        get_messages(channel_information: dict) -> list:
            Retrieves messages from a specified channel.
        save_messages(messages: list, channel_information: dict, folder_name: str):
            Saves the retrieved messages to a JSON file in the specified folder.
    """
    
    def __init__(self) -> None:
        """
        Initializes the Telegram_Scraper instance.
        """
        self.project_path = Path(Path(__file__).resolve().parent)
        self.session_counter = 0
        with open(self.make_path("Utils/config.json"), 'r', encoding='utf-8') as file:
            self.config = json.load(file)
        self.load_credential_keys()

    def make_path(self, extension:str):
        return str(self.project_path / extension)
    
    def load_credential_keys(self):
        """
        Loads credential keys from the configuration file.

        If 'alternating_configs' is enabled, loads multiple credential keys from 
        './Utils/Telegram_API_Credentials.json'. Otherwise, loads a single credential key.
        """
        if not self.config["alternating_configs"]:
            self.credential_keys = [self.config["config_file"]]
        else:
            with open(self.make_path("Utils/Telegram_API_Credentials.json"), 'r', encoding='utf-8') as file:
                self.credential_keys = list(json.load(file).keys())

    def load_credentials(self):
        """
        Loads the Telegram API credentials for the current session.

        Selects the appropriate credential key based on the session counter.
        """
        with open(self.make_path("Utils/Telegram_API_Credentials.json"), 'r', encoding='utf-8') as file:
            self.credentials = json.load(file)
        self.credentials = self.credentials[self.credential_keys[self.session_counter % len(self.credential_keys)]]
        
    def channel_iter(self):
        """
        Iterates over channel configuration files and yields their content.

        Loads channel configuration files from './Utils/Telegram_Channels/' and yields
        their content as dictionaries.

        Yields:
            dict: Channel configuration data.
        """
        path_list = glob(self.make_path("Utils/Telegram_Channels/*.json"))
        for path in tqdm(path_list, total=len(path_list), desc="Get Telegram Channels", leave=False):
            with open(path, "r", encoding="utf-8") as file:
                yield json.load(file)

    async def access_api(self, channel_name: str) -> list:
        """
        Asynchronously accesses the Telegram API to retrieve messages from a specified channel.

        Retrieves messages, parses them, and adds additional metadata such as channel name, 
        member count, and message link.

        Args:
            channel_name (str): The name of the Telegram channel to retrieve messages from.

        Returns:
            list: List of retrieved and parsed messages.
        """
        app = Client(self.credentials["scraper_name"], api_id=self.credentials["api_id"], api_hash=self.credentials["api_hash"])
        self.progress_bar = tqdm(total=self.config["limit"], desc=f"Get messages from: {channel_name}", leave=False)
        messages = list()
        try:
            async with app:
                member_count = await app.get_chat_members_count(channel_name)
            async with app:
                async for message in app.get_chat_history(channel_name, limit=self.config["limit"]):
                    message = self.parse(message)
                    message["Channel_Name"] = channel_name
                    message["Member_count"] = member_count
                    message["Link"] = f"https://t.me/{channel_name}/{message['Message_ID']}"
                    messages.append(message)
                    self.progress_bar.update(1)
        except FloodWait as e:
            if self.config["wait_for_flood"]:
                await asyncio.sleep(e.value)
            else:
                self.progress_bar.close()
                messages = None
        except RPCError as e:
            self.progress_bar.close()
            messages = None
        return messages

    def get_messages(self, channel_information: dict) -> list:
        """
        Retrieves messages from a specified channel.

        Loads the API credentials and retrieves messages from the channel asynchronously.

        Args:
            channel_information (dict): Information about the channel to retrieve messages from.

        Returns:
            list: List of retrieved messages.
        """
        self.load_credentials()
        messages = asyncio.run(self.access_api(channel_name=channel_information["Channel_Name"]))
        self.session_counter += 1
        return messages

    def save_messages(self, messages: list, channel_information: dict, folder_name: str):
        """
        Saves the retrieved messages to a JSON file in the specified folder.

        Creates the folder if it does not exist and writes each message as a JSON string.

        Args:
            messages (list): List of retrieved messages.
            channel_information (dict): Information about the channel.
            folder_name (str): The folder to save the messages in.
        """
        if messages is not None:
            folder_name = self.make_path(f"Results/{folder_name}")
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            file_name = os.path.join(folder_name, f"{channel_information['Channel_Name']}.json")
            with open(file_name, 'w', encoding='utf-8') as file:
                for message in messages:
                    json_string = json.dumps(message, ensure_ascii=False)
                    file.write(json_string + '\n')

    def scrape(self):
        folder_name = datetime.datetime.now().strftime('D%d%m%Y_T%H%M%S')
        for idx, channel_information in enumerate(self.channel_iter()):
            messages = self.get_messages(channel_information=channel_information)
            self.save_messages(messages=messages, channel_information=channel_information, folder_name=folder_name)
            if self.config["random_periods"]:
                time.sleep(np.random.uniform(low=1, high=8))
        return folder_name
