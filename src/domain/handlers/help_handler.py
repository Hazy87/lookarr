from telegram import Update
from telegram.ext import CallbackContext

from src.domain.handlers.interfaces.ihelp_handler import IHelpHandler


class HelpHandler(IHelpHandler):
    @staticmethod
    def help(update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Use /start to tests this bot.")
