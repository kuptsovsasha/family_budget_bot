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
from .handlers.report_handler import (
    show_report_options,
    generate_report,
    handle_custom_date_start,
    handle_custom_date_end,
    cancel_date_selection
)
from config import (
    MAIN_MENU,
    SELECT_CATEGORY,
    ENTER_AMOUNT,
    ADD_RECORD,
    CONFIRM_RECORD,
    GENERATE_REPORT,
    CUSTOM_DATE_START,
    CUSTOM_DATE_END
)


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
            CUSTOM_DATE_START: [
                CallbackQueryHandler(cancel_date_selection, pattern="^cancel_date$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_date_start)
            ],
            CUSTOM_DATE_END: [
                CallbackQueryHandler(cancel_date_selection, pattern="^cancel_date$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_date_end)
            ],
        },
        fallbacks=[
            CommandHandler("cancel", cancel),
            CommandHandler("start", start)
        ],
    )

    return conv_handler
