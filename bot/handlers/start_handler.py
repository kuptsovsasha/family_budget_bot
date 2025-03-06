from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from ..keyboards import Keyboards
from config import MAIN_MENU


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Start the conversation and introduce the bot to the user.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! Welcome to your Family Budget Tracker.\n\n"
        "I can help you track your income and expenses and generate reports."
    )
    return await show_main_menu(update, context)


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Show the main menu to the user.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The MAIN_MENU state
    """
    reply_markup = Keyboards.main_menu_keyboard()

    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text="Що ви хотіли б додати?",
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text="Що ви хотіли б додати?",
            reply_markup=reply_markup
        )

    return MAIN_MENU


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancel the current operation and end the conversation.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: ConversationHandler.END
    """
    await update.message.reply_text("Operation cancelled.")
    context.user_data.clear()
    return ConversationHandler.END


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Display help information to the user.

    Args:
        update: The update object
        context: The context object
    """
    help_text = (
        "💰 *Family Budget Bot Help* 💰\n\n"
        "*Main Commands:*\n"
        "/start - Start the bot and show main menu\n"
        "/help - Show this help message\n"
        "/cancel - Cancel current operation\n\n"

        "*How to use:*\n"
        "1. Add income or expenses by selecting the appropriate option\n"
        "2. Choose a category for your transaction\n"
        "3. Enter the amount\n"
        "4. Optionally add a description\n"
        "5. Confirm your entry\n\n"

        "Generate reports to see your financial status for different time periods."
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')
