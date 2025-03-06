from telegram.ext import Application, CommandHandler
from config import TELEGRAM_TOKEN, logger
from db import setup_database
from bot import setup_conversation_handler
from bot.handlers.start_handler import help_command


def main():
    """
    Main function to start the bot
    """
    # Set up database
    logger.info("Setting up SQLite database...")
    setup_database()

    # Initialize the bot
    logger.info("Starting the bot...")
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add conversation handler
    conversation_handler = setup_conversation_handler()
    application.add_handler(conversation_handler)

    # Add standalone command handlers
    application.add_handler(CommandHandler("help", help_command))

    # Start the Bot
    logger.info("Bot is running!")
    application.run_polling()


if __name__ == "__main__":
    main()
