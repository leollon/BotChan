import logging

from logbot import updater

logging.basicConfig(
    format='%(asciitime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

updater.start_polling()
