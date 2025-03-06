from telegram.ext import ConversationHandler, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers.start_handler import start, show_main_menu, cancel, help_command
from bot.handlers.transaction_handler import (
    handle_main_menu,
    show_categories,
    handle_category_selection,
    handle_amount,
    handle_confirmation,
    handle_description
)
from .handlers.report_handler import show_report_options, generate_report
from config import MAIN_MENU, SELECT_CATEGORY, ENTER_AMOUNT, ADD_RECORD, CONFIRM_RECORD, GENERATE_REPORT


def setup_conversation_handler():
    """
    Create and return the conversation handler for the bot

    Returns:
        ConversationHandler: The configured conversation handler
    """
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [
                CallbackQueryHandler(handle_main_menu)
            ],
            SELECT_CATEGORY: [
                CallbackQueryHandler(handle_category_selection)
            ],
            ENTER_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount)
            ],
            ADD_RECORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)
            ],
            CONFIRM_RECORD: [
                CallbackQueryHandler(handle_confirmation)
            ],
            GENERATE_REPORT: [
                CallbackQueryHandler(generate_report)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start)
        ],
    )

    return conv_handler
