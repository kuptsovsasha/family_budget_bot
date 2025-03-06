from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
from ..keyboards import Keyboards
from db import DBHandler
from .start_handler import show_main_menu
from config import GENERATE_REPORT


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

    # Get transaction summary
    summary = DBHandler.get_category_summary(start_date, end_date)

    # Format the report
    report = f"📊 Звіт за {period_name} 📊\n\n"

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

    report += f"\nЗагальні витрати: {total_income:.2f}\n\n"

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

    await query.edit_message_text(
        text=report,
        reply_markup=reply_markup
    )

    return GENERATE_REPORT
