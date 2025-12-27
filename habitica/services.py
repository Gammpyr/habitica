import logging

import requests

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL

logger = logging.getLogger(__name__)


def send_telegram_message(chat_id, message):
    try:
        params = {
            "text": message,
            "chat_id": chat_id,
        }
        response = requests.get(f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", params=params)
        return response
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {e}", exc_info=True)
        return None
