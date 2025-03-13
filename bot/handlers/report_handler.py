from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from ..keyboards import Keyboards
from db import DBHandler
from .start_handler import show_main_menu
from config import GENERATE_REPORT, CUSTOM_DATE_START, CUSTOM_DATE_END


async def show_report_options(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Show report options to the user.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The GENERATE_REPORT state
    """
    reply_markup = Keyboards.report_options_keyboard()

    await update.callback_query.edit_message_text(
        text="Вибиріть за який період потрібен звіт:",
        reply_markup=reply_markup
    )

    return GENERATE_REPORT


async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Generate and display a financial report based on the selected time period.

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

    if query.data == "report_custom":
        # Handle custom date range selection
        await query.edit_message_text(
            "Введіть початкову дату у форматі DD.MM.YYYY (наприклад, 01.03.2024):",
            reply_markup=Keyboards.date_cancel_keyboard()
        )
        return CUSTOM_DATE_START

    user_id = update.effective_user.id
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Set date range based on selection
    if query.data == "report_today":
        start_date = today
        end_date = today + timedelta(days=1) - timedelta(microseconds=1)
        period_name = "Сьогодні"
    elif query.data == "report_week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
        period_name = "Цей тиждень"
    elif query.data == "report_month":
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(microseconds=1)
        period_name = "Цей місяць"

    # Generate and show the report
    await show_formatted_report(update, context, start_date, end_date, period_name)
    return GENERATE_REPORT


async def handle_custom_date_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the start date input for custom date range reports.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    date_text = update.message.text.strip()

    try:
        # Parse the date in DD.MM.YYYY format
        start_date = datetime.strptime(date_text, "%d.%m.%Y").replace(hour=0, minute=0, second=0, microsecond=0)

        # Store the start date in context
        context.user_data["custom_start_date"] = start_date

        # Ask for end date
        await update.message.reply_text(
            "Введіть кінцеву дату у форматі DD.MM.YYYY (наприклад, 31.03.2024):",
            reply_markup=Keyboards.date_cancel_keyboard()
        )
        return CUSTOM_DATE_END

    except ValueError:
        await update.message.reply_text(
            "Неправильний формат дати. Будь ласка, введіть дату у форматі DD.MM.YYYY (наприклад, 01.03.2024):",
            reply_markup=Keyboards.date_cancel_keyboard()
        )
        return CUSTOM_DATE_START


async def handle_custom_date_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Handle the end date input for custom date range reports.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    date_text = update.message.text.strip()

    try:
        # Parse the end date in DD.MM.YYYY format
        end_date = datetime.strptime(date_text, "%d.%m.%Y").replace(hour=23, minute=59, second=59, microsecond=999999)

        start_date = context.user_data.get("custom_start_date")

        # Validate date range
        if end_date < start_date:
            await update.message.reply_text(
                "Кінцева дата не може бути раніше початкової. Будь ласка, введіть правильну кінцеву дату:",
                reply_markup=Keyboards.date_cancel_keyboard()
            )
            return CUSTOM_DATE_END

        # Format the date range for display
        start_date_str = start_date.strftime("%d.%m.%Y")
        end_date_str = end_date.strftime("%d.%m.%Y")
        period_name = f"{start_date_str} - {end_date_str}"

        # Generate and show the report
        await show_formatted_report(update, context, start_date, end_date, period_name)

        # Clear the stored dates
        if "custom_start_date" in context.user_data:
            del context.user_data["custom_start_date"]

        return GENERATE_REPORT

    except ValueError:
        await update.message.reply_text(
            "Неправильний формат дати. Будь ласка, введіть дату у форматі DD.MM.YYYY (наприклад, 31.03.2024):",
            reply_markup=Keyboards.date_cancel_keyboard()
        )
        return CUSTOM_DATE_END


async def cancel_date_selection(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    Cancel the custom date range selection process.

    Args:
        update: The update object
        context: The context object

    Returns:
        int: The next conversation state
    """
    # Clear any stored dates
    if "custom_start_date" in context.user_data:
        del context.user_data["custom_start_date"]

    await update.callback_query.answer()
    return await show_report_options(update, context)


async def show_formatted_report(update: Update, context: ContextTypes.DEFAULT_TYPE, start_date, end_date, period_name):
    """
    Format and display a financial report for the given date range.

    Args:
        update: The update object
        context: The context object
        start_date: The start date of the report period
        end_date: The end date of the report period
        period_name: The name of the period for display
    """
    # Get transaction summary
    summary = DBHandler.get_category_summary(start_date, end_date)

    # Format the report
    report = f"📊 Звіт за період: {period_name} 📊\n\n"

    total_income = 0
    total_expense = 0

    # Process income
    report += "💰 Дохід:\n"
    has_income = False
    for item in summary:
        if item['type'] == 'income':
            has_income = True
            amount = float(item['total'])
            total_income += amount
            report += f"• {item['category']}: {amount:.2f}\n"

    if not has_income:
        report += "• Нема доходів за вибраний період\n"

    report += f"\nЗагальні доходи: {total_income:.2f}\n\n"

    # Process expenses
    report += "💸 Витрати:\n"
    has_expenses = False
    for item in summary:
        if item['type'] == 'expense':
            has_expenses = True
            amount = float(item['total'])
            total_expense += amount
            report += f"• {item['category']}: {amount:.2f}\n"

    if not has_expenses:
        report += "• Нема витрат за вибраний період\n"

    report += f"\nЗагальні витрати: {total_expense:.2f}\n\n"

    # Balance
    balance = total_income - total_expense
    status = "✅ Баланс" if balance >= 0 else "⚠️ DEFICIT"
    report += f"{status}: {abs(balance):.2f}\n"

    if total_income > 0:
        savings_rate = (balance / total_income) * 100 if balance > 0 else 0
        report += f"Баланс у відсотках: {savings_rate:.1f}%\n"

    # Add navigation buttons
    reply_markup = Keyboards.report_navigation_keyboard()

    # Determine if we need to edit a message or send a new one
    if update.callback_query:
        await update.callback_query.edit_message_text(
            text=report,
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            text=report,
            reply_markup=reply_markup
        )
