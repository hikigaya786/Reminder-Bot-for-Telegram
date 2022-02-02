from ast import Call
from distutils.command.config import config
import re
from telegram.ext import Updater, CallbackContext, CommandHandler
from telegram import Update
import logging
from datetime import date, datetime, timedelta


logging.basicConfig(filename="Logs.txt",
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update: Update, context: CallbackContext) -> None:
    """logging error caused by Updates."""
    logger.warning(f"Update {update} caused error {context.error}")


def start(update: Update, context: CallbackContext) -> None:
    """Welcome msg"""
    context.bot.send_message(
        text="Hi I am a Reminder Bot I can send you reminders", chat_id=update.effective_chat.id)


def reminder_msg(context: CallbackContext) -> None:
    """The massage deliverd at the time of reminder"""
    job = context.job   # setting up the job
    context.bot.send_message(
        job.context, text="BEEP BEEP!!!!!\nYour Reminder is here.")


def set(update: Update, context: CallbackContext) -> None:

    # chat_id = update.message.chat_id
    try:
        chat_id = update.message.chat_id
        # user_reply should be of type /set 12:15 PM
        user_reply = update.effective_message.text
        # strip /set from the user reply
        reminder_time = user_reply.replace(r"/set", "")

        today = datetime.today().date()
        now = datetime.now()

        reminder_time = str(today) + reminder_time
        reminder_time = datetime.strptime(reminder_time, "%Y-%m-%d %I:%M %p")

        time_difference = (reminder_time - now).total_seconds()
        print(time_difference)
        if time_difference < 0:
            update.message.reply_text("You can not set reminder of past")
            return

        context.job_queue.run_once(
            reminder_msg, time_difference, context=chat_id, name=str(chat_id))
        text = "Timer Set Succesfully"
        update.message.reply_text(text)

    except (ValueError, IndexError):

        context.bot.send_message(
            text="Usage /set_time HH:MM AM/PM", chat_id=update.effective_chat.id)


def help(update: Update, context: CallbackContext) -> None:
    """help handler"""
    context.bot.send_message(
        text="Send the time in format HH:MM AM/PM", chat_id=update.effective_chat.id)


def main():
    import config

    Token = config.Token
    updater = Updater(token=Token, use_context=True)
    dispathcer = updater.dispatcher

    start_handler = CommandHandler('start', start)
    set_handler = CommandHandler('set', set)
    help_handler = CommandHandler('help', help)

    dispathcer.add_handler(start_handler)
    dispathcer.add_handler(set_handler)
    dispathcer.add_handler(help_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
