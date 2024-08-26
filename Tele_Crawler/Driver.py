import logging
import traceback
from TelegramMongoDB import TelegramMongoDB
from Telegram_API_Request import Telegram_Scraper

log_file_path = "./exception_log.log"
logging.basicConfig(filename=log_file_path, level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    try:
        folder_name = Telegram_Scraper().scrape()
        tmdb = TelegramMongoDB()
        tmdb.main(folder_name)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"An exception occurred: {e}",traceback.format_exc())
        logging.error(f"An exception occurred: {e}", exc_info=True)
        raise Exception