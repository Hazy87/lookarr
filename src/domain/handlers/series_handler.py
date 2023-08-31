from telegram import Update
from telegram.ext import CallbackContext
from kink import inject

from domain.checkers.authentication_checker import check_user_is_authenticated
from domain.checkers.conversation_checker import check_conversation
from domain.handlers.interfaces.imedia_handler import IMediaHandler
from domain.handlers.interfaces.iseries_handler import ISeriesHandler
from domain.handlers.messages_handler import MessagesHandler
from interface.keyboard import Keyboard
from logger import ILogger


@inject
class SeriesHandler(ISeriesHandler):
    def __init__(self, logger: ILogger, conversation_handler: IMediaHandler):
        self._logger = logger,
        self._conversation_handler = conversation_handler

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def set_quality(self, update: Update, context: CallbackContext):
        query = update.callback_query

        if not context.user_data.get("quality_profile"):
            context.user_data["quality_profile"] = query.data.removeprefix("SonarrQuality: ")

        self.select_season(update, context)

    @check_user_is_authenticated
    @check_conversation(["update_msg", "type"])
    def select_season(self, update: Update, context: CallbackContext):
        MessagesHandler.update_message(context, update, ".. 👀")

        query = update.callback_query

        position = context.user_data["position"]

        if not "seasons" in context.user_data:
            self._set_seasons(context, position)
        else:
            self._update_selected_seasons(query, context)

        seasons = context.user_data["seasons"]

        keyboard = Keyboard.seasons(seasons)

        MessagesHandler.update_message(context, update, "Select Season:", keyboard)

    @staticmethod
    def _set_seasons(context: CallbackContext, position: int):
        seasons = context.user_data['results'][position]['seasons']
        seasons = [season for season in seasons if season["seasonNumber"] != 0]
        for season in seasons:
            season["selected"] = False

        context.user_data["seasons"] = seasons

    @staticmethod
    def _update_selected_seasons(query, context: CallbackContext):
        selected_season = query.data.removeprefix("SelectSeason: ")
        if selected_season in ["All", "Unselect"]:
            selected = True if selected_season == "All" else False
            for season in context.user_data["seasons"]:
                season["selected"] = selected
        else:
            for season in context.user_data["seasons"]:
                if season["seasonNumber"] == int(selected_season):
                    season["selected"] = not season["selected"]
                    break
