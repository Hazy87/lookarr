from kink import di
from logger import ILogger, Logger

di[ILogger] = Logger(__name__)

from typing import List
import requests
from constants import CONFIG_FULL_PATH
from domain.config.app_config import Config
from domain.config.config_loader import ConfigLoader
from domain.handlers.help_handler import HelpHandler
from domain.handlers.interfaces.ihelp_handler import IHelpHandler
from domain.handlers.interfaces.imovie_handler import IMovieHandler
from domain.handlers.movie_handler import MovieHandler
from domain.handlers.series_handler import SeriesHandler
from domain.handlers.interfaces.iseries_handler import ISeriesHandler
from infrastructure.interfaces.IDatabase import IDatabase
from infrastructure.db.sqlite import Database
from infrastructure.interfaces.imedia_server_factory import IMediaServerFactory
from infrastructure.interfaces.imedia_server_repository import IMediaServerRepository
from infrastructure.media_server_factory import MediaServerFactory
from domain.auth.authentication import Auth
from domain.auth.interfaces.iauthentication import IAuth
from infrastructure.media_server_repository import IMediaServerRepositoryBase, MediaServer
from infrastructure.radarr.radarr import Radarr
from domain.handlers.authentication_handler import AuthHandler
from domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from domain.handlers.media_handler import MediaHandler
from domain.handlers.interfaces.imedia_handler import IMediaHandler
from domain.handlers.interfaces.istop_handler import IStopHandler
from domain.handlers.stop_handler import StopHandler
from infrastructure.sonarr.sonarr import Sonarr


def configure_services() -> None:
    di[Config] = ConfigLoader().load_config(CONFIG_FULL_PATH)
    di[IDatabase] = Database()
    di[IAuth] = Auth()
    di["client"] = requests

    di[IMediaServerRepositoryBase] = MediaServer()

    di[List[IMediaServerRepository]] = [
        Radarr(),
        Sonarr()
    ]

    di[IMediaServerFactory] = MediaServerFactory()
    di[IAuthHandler] = AuthHandler()
    di[IMediaHandler] = MediaHandler()
    di[ISeriesHandler] = SeriesHandler()
    di[IMovieHandler] = MovieHandler()
    di[IStopHandler] = StopHandler()
    di[IHelpHandler] = HelpHandler()
