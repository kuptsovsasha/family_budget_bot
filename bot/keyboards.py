from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Keyboards:
    """
    Class for creating keyboard layouts used in the bot
    """

    @staticmethod
    def main_menu_keyboard():
        """Create the main menu keyboard"""
        keyboard = [
            [InlineKeyboardButton("Додати дохід", callback_data="add_income")],
            [InlineKeyboardButton("Додати витрати", callback_data="add_expense")],
            [InlineKeyboardButton("Звіт", callback_data="reports")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def categories_keyboard(categories):
        """
        Create a keyboard with categories

        Args:
            categories (list): List of (id, name) tuples

        Returns:
            InlineKeyboardMarkup: Keyboard with category buttons
        """
        keyboard = []
        for cat_id, cat_name in categories:
            keyboard.append([InlineKeyboardButton(cat_name, callback_data=f"cat_{cat_id}")])

        keyboard.append([InlineKeyboardButton("Назад", callback_data="back_to_main")])
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def confirmation_keyboard(with_description=False):
        """
        Create a keyboard for transaction confirmation

        Args:
            with_description (bool): Whether to include add description button

        Returns:
            InlineKeyboardMarkup: Confirmation keyboard
        """
        if with_description:
            keyboard = [
                [InlineKeyboardButton("Додати опис", callback_data="add_description")],
                [InlineKeyboardButton("Підтвердити", callback_data="confirm")],
                [InlineKeyboardButton("Скасувати", callback_data="cancel")]
            ]
        else:
            keyboard = [
                [InlineKeyboardButton("Підтвердити", callback_data="confirm")],
                [InlineKeyboardButton("Скасувати", callback_data="cancel")]
            ]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def report_options_keyboard():
        """Create the report options keyboard"""
        keyboard = [
            [InlineKeyboardButton("Сьогодні", callback_data="report_today")],
            [InlineKeyboardButton("Цей тиждень", callback_data="report_week")],
            [InlineKeyboardButton("Цей місяць", callback_data="report_month")],
            [InlineKeyboardButton("Назад", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def report_navigation_keyboard():
        """Create the keyboard for report navigation"""
        keyboard = [
            [InlineKeyboardButton("Назад до звітів", callback_data="reports")],
            [InlineKeyboardButton("Головне меню", callback_data="back_to_main")]
        ]
        return InlineKeyboardMarkup(keyboard)
