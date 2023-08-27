from kink import di, inject
from src.logger import ILogger, Logger

di[ILogger] = Logger(__name__)

from typing import List
from os import path, makedirs

from src.constants import CONFIG_FULL_PATH
from src.domain.config.app_config import ConfigLoader, Config
from src.domain.handlers.help_handler import HelpHandler
from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler
from src.domain.validators.env_validator import EnvValidator
from src.infrastructure.interfaces.IDatabase import IDatabase
from src.infrastructure.db.sqlite import Database
from src.infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from src.infrastructure.interfaces.imedia_server import IMediaServerRepository
from src.infrastructure.media_server_factory import MediaServerFactory
from src.domain.auth.authentication import Auth
from src.domain.auth.interfaces.iauthentication import IAuth
from src.infrastructure.radarr.radarr import Radarr
from src.domain.handlers.authentication_handler import AuthHandler
from src.domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from src.domain.handlers.conversation_handler import SearchHandler
from src.domain.handlers.interfaces.iconversation_handler import ISearchHandler
from src.domain.handlers.interfaces.istop_handler import IStopHandler
from src.domain.handlers.stop_handler import StopHandler

di[Config] = ConfigLoader(CONFIG_FULL_PATH)
di[IDatabase] = Database()
di[IAuth] = Auth()
di[List[IMediaServerRepository]] = [Radarr()]
di[IMediaServerFactory] = MediaServerFactory()
di[IAuthHandler] = AuthHandler()
di[ISearchHandler] = SearchHandler()
di[IStopHandler] = StopHandler()
di[IHelpHandler] = HelpHandler()


@inject
def initialise(db: IDatabase, config: Config) -> None:
    if not path.exists("logs"):
        makedirs("logs")

    db.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled)
    if not env.is_valid:
        raise ValueError(
            f"Unable to start app as the following required env variables are missing: {''.join(env.reasons)}")
