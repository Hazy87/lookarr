from os import path

ROOT_PATH = path.dirname(path.dirname(path.normpath(__file__)))
USER_CONFIG_PATH = f"{ROOT_PATH}/user_config"
CONFIG_FULL_PATH = f"{USER_CONFIG_PATH}/config.yml"
LOOKAR_DB_PATH = f"{USER_CONFIG_PATH}/lookar.db"

LANGUAGES_PATH = "languages"
LOG_FULL_PATH = "logs/lookarr.log"
SUPPORTED_LANGUAGES = ["en-us"]
YOUTUBE_BASE_URL = "https://www.youtube.com/watch?v="
DEFAULT_IMAGE = "https://artworks.thetvdb.com/banners/images/missing/movie.jpg"
