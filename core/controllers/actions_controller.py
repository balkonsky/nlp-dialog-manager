from sys import platform
import shutil
import os
import json
import requests as req
from loguru import logger
from core.config import Settings

settings = Settings()

__all__ = ['send_message', 'redirect_chat', 'get_file', 'close_chat']


def send_message(chat_id, message):
    # TODO
    _make_request(url, data)


def redirect_chat(language, dep_key, chat_id):
    # TODO
    _make_request(url, data)


def close_chat(chat_id):
    # TODO
    _make_request(url, data)


def get_file(file_url, file_name):
    # TODO
    pass


def _make_request(url, data):
    # TODO
    pass
