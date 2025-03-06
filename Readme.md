# Family Budget Telegram Bot

A Telegram bot that helps track family budget by allowing users to record income and expenses and generate financial reports.

## Features

- **Simple Database Structure**: SQLite database for easy setup with no additional dependencies
- **User-Friendly Interface**: Button-based navigation throughout the bot
- **Transaction Management**:
  - Add income or expenses
  - Choose from predefined categories
  - Add optional descriptions
- **Comprehensive Reports**:
  - View reports for today, current week, or current month
  - See income and expenses by category
  - Calculate balance, surplus/deficit, and savings rate

## Project Structure

```
family_budget_bot/
├── config.py                # Configuration settings
├── db/
│   ├── __init__.py
│   ├── models.py            # Database models and constants
│   └── sqlite_handler.py    # SQLite database operations
├── bot/
│   ├── __init__.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start_handler.py
│   │   ├── transaction_handler.py
│   │   └── report_handler.py
│   ├── conversations.py     # Conversation states and flows
│   └── keyboards.py         # Keyboard layouts
└── main.py                  # Entry point
```

## Setup Instructions

1. Clone this repository or download the source code

2. Install the required Python packages:
   ```bash
   pip install python-telegram-bot
   ```

3. Get a Telegram Bot Token from @BotFather and update the `TELEGRAM_TOKEN` in `config.py`

4. Run the bot:
   ```bash
   python main.py
   ```

## How to Use the Bot

1. Start a chat with your bot on Telegram
2. Use the `/start` command to initialize the bot
3. Navigate through the menu to:
   - Add income
   - Add expenses
   - View reports
4. Follow the prompts to record transactions
5. Generate reports to analyze your budget

## Customization

You can easily customize the bot by:

1. Modifying the income and expense categories in `db/models.py`
2. Changing the bot's responses in the handler files
3. Adding new features by extending the existing code structure

## Technical Details

- Built with Python 3.7+
- Uses python-telegram-bot framework
- SQLite database for data storage
- Modular and maintainable code structure

## Troubleshooting

If you encounter any issues:

1. Check that your Telegram token is correctly set in `config.py`
2. Ensure you have the necessary permissions to create and write to files in the bot's directory
3. Check the log output for error messages

## License

This project is open-source and free to use.