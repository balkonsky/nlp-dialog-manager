from os import path, environ
from pydantic import BaseSettings
from dotenv import load_dotenv


class Settings(BaseSettings):
    """App default configuration"""
    base = path.abspath(path.dirname(__file__))

    if path.exists('.env'):
        load_dotenv('.env')

    redis_url: str = environ.get('REDIS_URL', default='redis://')
