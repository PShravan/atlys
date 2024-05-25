import os

from starlette.config import Config

env_file = ".env"

config = Config()
if os.path.exists(env_file):
    config = Config(env_file)

# Base
API_V1_PREFIX = config("API_V1_PREFIX", cast=str, default="/api/v1")
DEBUG = config("DEBUG", cast=bool, default=True)
PROJECT_NAME = config("PROJECT_NAME", cast=str, default="Data scraping API")
VERSION = config("VERSION", cast=str, default="1.0.0")
DENTAL_SITE_ENTRYPOINT = config(
    "DENTAL_SITE_ENTRYPOINT", cast=str, default="https://dentalstall.com/shop/"
)
