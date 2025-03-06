from telegram import Update
from telegram.ext import ContextTypes
from ..keyboards import Keyboards
from db import DBHandler
from .start_handler import show_main_menu
from .report_handler import show_report_options
from config import SELECT_CATEGORY, ENTER_AMOUNT, CONFIRM_RECORD, ADD_RECORD, MAIN_MENU


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle selections from the main menu.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    query = update.callback_query
    await query.answer()

    if query.data == "add_income":
        context.user_data["transaction_type"] = "income"
        return await show_categories(update, context)
    elif query.data == "add_expense":
        context.user_data["transaction_type"] = "expense"
        return await show_categories(update, context)
    elif query.data == "reports":
        return await show_report_options(update, context)

    return MAIN_MENU


async def show_categories(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Show category selection for income or expense.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The SELECT_CATEGORY state
    """
    transaction_type = context.user_data.get("transaction_type")
    categories = DBHandler.get_categories(transaction_type)

    reply_markup = Keyboards.categories_keyboard(categories)

    await update.callback_query.edit_message_text(
        text=f"Виберіть {transaction_type} категорію:",
        reply_markup=reply_markup
    )

    return SELECT_CATEGORY


async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the selection of a category.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    query = update.callback_query
    await query.answer()

    if query.data == "back_to_main":
        return await show_main_menu(update, context)

    # Extract category ID from callback data
    category_id = int(query.data.split("_")[1])
    context.user_data["category_id"] = category_id

    # Get category name for confirmation
    category_info = DBHandler.get_category_info(category_id)
    context.user_data["category_name"] = category_info['name']

    await query.edit_message_text(
        text=f"Вибрана категорія: {category_info['name']}.\nбудь ласка введіть суму:"
    )

    return ENTER_AMOUNT


async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the amount input from the user.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    amount_text = update.message.text.strip()

    try:
        amount = float(amount_text)
        if amount <= 0:
            await update.message.reply_text("Будь ласка введіть коректну суму.")
            return ENTER_AMOUNT

        context.user_data["amount"] = amount

        # Create confirmation message
        transaction_type = context.user_data.get("transaction_type")
        category_name = context.user_data.get("category_name")

        reply_markup = Keyboards.confirmation_keyboard(with_description=True)

        await update.message.reply_text(
            f"Ви додали {transaction_type} на {amount:.2f} у категорії '{category_name}'.\n"
            f"Хочете додати опис чи підтвердити цю дію?",
            reply_markup=reply_markup
        )

        return CONFIRM_RECORD

    except ValueError:
        await update.message.reply_text("Некоректна сума. Введіть числове значення.")
        return ENTER_AMOUNT


async def handle_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the transaction confirmation.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    query = update.callback_query
    await query.answer()

    if query.data == "cancel":
        await query.edit_message_text("Операцію відмінено.")
        return await show_main_menu(update, context)

    elif query.data == "add_description":
        await query.edit_message_text("Введіть короткий опис:")
        return ADD_RECORD

    elif query.data == "confirm":
        # Save transaction to database
        user_id = update.effective_user.id
        category_id = context.user_data.get("category_id")
        amount = context.user_data.get("amount")
        description = context.user_data.get("description", None)

        DBHandler.add_transaction(user_id, category_id, amount, description)

        await query.edit_message_text("Успішно додано!")

        # Clear user data
        context.user_data.clear()

        # Return to main menu
        return await show_main_menu(update, context)

    return CONFIRM_RECORD


async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the description input from the user.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    description = update.message.text.strip()
    context.user_data["description"] = description

    # Create confirmation message with description
    transaction_type = context.user_data.get("transaction_type")
    category_name = context.user_data.get("category_name")
    amount = context.user_data.get("amount")

    reply_markup = Keyboards.confirmation_keyboard(with_description=False)

    await update.message.reply_text(
        f"Ви додали {transaction_type} на {amount:.2f} у категорії '{category_name}'.\n"
        f"Опис: {description}\n\n"
        f"Підтвердити?",
        reply_markup=reply_markup
    )

    return CONFIRM_RECORD
