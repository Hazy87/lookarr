#!/usr/bin/env python

from os import environ, path, makedirs

from kink import inject
from dependencies.services import configure_services

from domain.handlers.interfaces.iauthentication_handler import IAuthHandler
from domain.handlers.interfaces.imedia_handler import IMediaHandler

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from domain.config.app_config import Config
from domain.handlers.interfaces.ihelp_handler import IHelpHandler
from domain.handlers.interfaces.imovie_handler import IMovieHandler
from domain.handlers.interfaces.istop_handler import IStopHandler
from domain.handlers.interfaces.iseries_handler import ISeriesHandler
from domain.validators.env_validator import EnvValidator
from infrastructure.interfaces.IDatabase import IDatabase


@inject
def initialise(db: IDatabase, config: Config) -> None:
    if not path.exists("logs"):
        makedirs("logs")

    db.initialise()
    env = EnvValidator()
    env.verify_required_env_variables_exist(config.radarr.enabled, config.sonarr.enabled)
    if not env.is_valid:
        raise ValueError(
            f"Unable to start app as the following required env variables are missing: {''.join(env.reasons)}")


@inject
def main(
        config: Config,
        authentication_handler: IAuthHandler,
        media_handler: IMediaHandler,
        series_handler: ISeriesHandler,
        movie_handler: IMovieHandler,
        stop_handler: IStopHandler,
        help_handler: IHelpHandler
) -> None:

    updater = Updater(environ.get("TELEGRAM_BOT_KEY"))

    updater.dispatcher.add_handler(CommandHandler(config.lookarr.search_all_command, media_handler.start_search))
    updater.dispatcher.add_handler(CallbackQueryHandler(movie_handler.add_to_library, pattern="RadarrQuality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(movie_handler.add_to_library, pattern="AddSeries"))
    updater.dispatcher.add_handler(CallbackQueryHandler(series_handler.set_quality, pattern="SonarrQuality"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.search_media, pattern="Sonarr|Radarr"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.change_option,
                                                        pattern="Next|Previous"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.get_folders, pattern="GetFolders"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.get_quality_profiles,
                                                        pattern="GetQualityProfiles"))
    updater.dispatcher.add_handler(CallbackQueryHandler(series_handler.select_season, pattern="SelectSeason"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.confirm_delete,
                                                        pattern="ConfirmDelete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(media_handler.delete, pattern="Delete"))
    updater.dispatcher.add_handler(CallbackQueryHandler(stop_handler.stop, pattern="Stop"))
    # updater.dispatcher.add_handler(CallbackQueryHandler(test_handlers.add, pattern="Add_This"))
    updater.dispatcher.add_handler(CommandHandler('help', help_handler.help))
    updater.dispatcher.add_handler(CommandHandler('auth', authentication_handler.authenticate))

    # Start bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    configure_services()
    initialise()
    main()
