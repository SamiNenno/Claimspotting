import datetime
import pyrogram

class MessageParser():
    """
    This class is supporting the Telegram Scraper by parsing the messages retrieved with Pyrogram.

    Methods:
        get_pyro_entity_type(entity: pyrogram.enums.MessageEntityType) -> str:
            Retrives information about the text like the use of emojis, links or hashtags.
            
        get_message_reactions(reactions) -> list:
            Retrieves reactions of post like forwards, likes or emojis.
            
        parse(message: dict) -> dict:
            Takes in a Pyrogram result and returns a parsed dictionary that represents one Telegram post including its metadata.
    """
    def get_pyro_entity_type(self, entity):
        if entity.type == pyrogram.enums.MessageEntityType.BOLD:
            return "BOLD"
        elif entity.type == pyrogram.enums.MessageEntityType.URL:
            return "URL"
        elif entity.type == pyrogram.enums.MessageEntityType.TEXT_LINK:
            return "TEXT_LINK"
        elif entity.type == pyrogram.enums.MessageEntityType.MENTION:
            return "MENTION"
        elif entity.type == pyrogram.enums.MessageEntityType. HASHTAG:
            return " HASHTAG"
        elif entity.type == pyrogram.enums.MessageEntityType.EMAIL:
            return "EMAIL"
        elif entity.type == pyrogram.enums.MessageEntityType. UNDERLINE:
            return " UNDERLINE"
        elif entity.type == pyrogram.enums.MessageEntityType.STRIKETHROUGH:
            return "STRIKETHROUGH"
        elif entity.type == pyrogram.enums.MessageEntityType.TEXT_MENTION:
            return "TEXT_MENTION"
        elif entity.type == pyrogram.enums.MessageEntityType. CUSTOM_EMOJI:
            return " CUSTOM_EMOJI"
        elif entity.type == pyrogram.enums.MessageEntityType.CASHTAG:
            return "CASHTAG"
        else:
            return "UNKNOWN"

    def get_message_reactions(self, reactions):
        if reactions is None:
            return None
        else:
            reaction_list = list()
            for r in reactions.reactions:
                reaction_list.append({"Emoji":r.emoji, "Count":r.count})
            return reaction_list

    def parse(self, message):
        message = message if isinstance(message, dict) else message.__dict__
        dct = {}
        dct["Message_ID"] = message['id']
        dct["User"] = None if message['from_user'] is None else dict(
            User_ID = message['from_user'].id,
            User_Name = message['from_user'].username,
            Is_deleted = message['from_user'].is_deleted,
            Is_bot = message['from_user'].is_bot,
            Is_restricted = message['from_user'].is_restricted,
            Is_scam = message['from_user'].is_scam,
            Is_fake = message['from_user'].is_fake,
            Is_premium = message['from_user'].is_premium,
        )
        dct["Publishing_datetime"] = message["date"].strftime('%Y-%m-%d %H:%M:%S')
        dct["Access_datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dct["Edit_datetime"] = None if message["edit_date"]is None else message["edit_date"].strftime('%Y-%m-%d %H:%M:%S')
        dct["Text"] = message["text"]
        dct["Caption"] = message["caption"]
        dct["Entities"] = None if message["entities"] is None else [{"Type":self.get_pyro_entity_type(entity), "Offset":entity.offset, "Length":entity.length, "Url":entity.url} for entity in message["entities"]]
        dct["Has_audio"] = message["audio"] is not None
        dct["Has_document"] = message["document"] is not None
        dct["Has_sticker"] = message["sticker"] is not None
        dct["Has_animation"] = message["animation"] is not None
        dct["Has_video"] = message["video"] is not None
        dct["Views"] = message["views"]
        dct["Forwards"] = message["forwards"]
        dct["Reactions"] = self.get_message_reactions(message["reactions"])
        return dct